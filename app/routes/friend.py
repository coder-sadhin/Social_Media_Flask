from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from app.models.user import User
from app.models.friendship import Friendship

friend = Blueprint('friend', __name__, url_prefix='/friend')


# 1. SEND REQUEST
@friend.route('/send/<int:user_id>')
@login_required
def send_request(user_id):
    if user_id == current_user.id:
        flash("You cannot add yourself.", "danger")
        return redirect(request.referrer or url_for("main.home"))

    # Check if any relationship already exists (pending or accepted)
    existing = Friendship.query.filter(
        ((Friendship.sender_id == current_user.id) & (Friendship.receiver_id == user_id)) |
        ((Friendship.sender_id == user_id) & (Friendship.receiver_id == current_user.id))
    ).first()

    if not existing:
        new_req = Friendship(sender_id=current_user.id, receiver_id=user_id, status='pending')
        db.session.add(new_req)
        db.session.commit()
        flash("Friend request sent!", "success")
    else:
        flash("A request is already pending or you are already friends.", "info")
    
    return redirect(request.referrer or url_for("main.home"))

# 2. ACCEPT REQUEST (Using user_id is easier for the UI)
@friend.route('/accept/<int:user_id>')
@login_required
def accept_request(user_id):
    # Security: Ensure I am the receiver of this specific user's request
    req = Friendship.query.filter_by(
        sender_id=user_id, 
        receiver_id=current_user.id, 
        status='pending'
    ).first_or_404()

    req.status = 'accepted'
    db.session.commit()
    flash("Friend request accepted!", "success")
    return redirect(request.referrer or url_for("main.home"))

# 3. REJECT / CANCEL / UNFRIEND (The "Remove" Logic)
@friend.route('/remove/<int:user_id>')
@login_required
def remove_friendship(user_id):
    # Find the friendship regardless of who sent it
    f = Friendship.query.filter(
        ((Friendship.sender_id == current_user.id) & (Friendship.receiver_id == user_id)) |
        ((Friendship.sender_id == user_id) & (Friendship.receiver_id == current_user.id))
    ).first()

    if f:
        db.session.delete(f)
        db.session.commit()
        flash("Friendship or request removed.", "info")
    
    return redirect(request.referrer or url_for("main.home"))