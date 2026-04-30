from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy import desc

from app import db
from app.models.post import Post
from app.models.user import User
from app.models.friendship import Friendship

main = Blueprint('main', __name__)


@main.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    return redirect(url_for('auth.login'))


@main.route('/feed')
@login_required
def feed():
    friends = current_user.get_friends()
    friend_ids = [u.id for u in friends]
    visible_user_ids = [current_user.id] + friend_ids

    posts = (
        Post.query
        .filter(Post.user_id.in_(visible_user_ids))
        .order_by(desc(Post.date_posted))
        .all()
    )

    suggestions = (
        User.query
        .filter(User.id != current_user.id)
        .order_by(User.created_at.desc())
        .limit(8)
        .all()
    )

    rel_map = {}
    if suggestions:
        suggestion_ids = [u.id for u in suggestions]
        rels = Friendship.query.filter(
            ((Friendship.sender_id == current_user.id) & (Friendship.receiver_id.in_(suggestion_ids))) |
            ((Friendship.receiver_id == current_user.id) & (Friendship.sender_id.in_(suggestion_ids)))
        ).all()

        for r in rels:
            other_id = r.receiver_id if r.sender_id == current_user.id else r.sender_id
            if r.status == 'accepted':
                rel_map[other_id] = 'friends'
            else:
                rel_map[other_id] = 'sent' if r.sender_id == current_user.id else 'received'

        for u in suggestions:
            rel_map.setdefault(u.id, 'none')

    return render_template('index.html', posts=posts, suggestions=suggestions, rel_map=rel_map, friends=friends)


@main.route('/posts', methods=['POST'])
@login_required
def create_post():
    content = (request.form.get('content') or '').strip()
    if not content:
        flash('Write something before posting.', 'danger')
        return redirect(url_for('main.feed'))

    post = Post(content=content, user_id=current_user.id)
    db.session.add(post)
    db.session.commit()

    flash('Posted!', 'success')
    return redirect(url_for('main.feed'))
