from app import db
from datetime import datetime

class Friendship(db.Model):
    __tablename__ = "friendships"

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(db.String(20), default="pending")  # pending, accepted, rejected

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Prevent duplicate requests
    __table_args__ = (
        db.UniqueConstraint("sender_id", "receiver_id", name="unique_friendship"),
    )