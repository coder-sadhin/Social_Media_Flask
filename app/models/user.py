from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, default="")
    profile_image = db.Column(db.String(255), default="default.png")

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # all friendships
    sent_requests = db.relationship(
        "Friendship",
        foreign_keys="Friendship.sender_id",
        backref="sender",
        lazy="dynamic"
    )
    received_requests = db.relationship(
        "Friendship",
        foreign_keys="Friendship.receiver_id",
        backref="receiver",
        lazy="dynamic"
    )
    # Relationships (important for future)
    posts = db.relationship("Post", backref="author", lazy=True)

    # Helper method to get friends list (Accepted only)
    def get_friends(self):
        # Users who sent me requests I accepted
        received = db.session.query(User).join(Friendship, User.id == Friendship.sender_id).filter(Friendship.receiver_id == self.id, Friendship.status == 'accepted').all()
        # Users I sent requests to who accepted
        sent = db.session.query(User).join(Friendship, User.id == Friendship.receiver_id).filter(Friendship.sender_id == self.id, Friendship.status == 'accepted').all()
        return received + sent

    def is_friend(self, user):
        return Friendship.query.filter(
            ((Friendship.sender_id == self.id) & (Friendship.receiver_id == user.id)) |
            ((Friendship.sender_id == user.id) & (Friendship.receiver_id == self.id))
        ).filter_by(status="accepted").first() is not None
        
    def __repr__(self):
        return f"<User {self.username}>"