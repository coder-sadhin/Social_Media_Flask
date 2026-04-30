from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.user import User
from app.models.post import Post

user_bp = Blueprint('user', __name__, url_prefix='/u')

@user_bp.route('/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    posts = (
        Post.query
        .filter_by(user_id=user.id)
        .order_by(Post.date_posted.desc())
        .all()
    )

    is_me = current_user.id == user.id

    return render_template('profile.html', profile_user=user, posts=posts, is_me=is_me)
