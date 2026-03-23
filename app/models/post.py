from app import db
from datetime import datetime, timezone

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    
    # The actual text of the post (optional if only uploading image)
    content = db.Column(db.Text, nullable=True) 
    
    # The image path, stored as a string (optional if only posting text)
    post_image = db.Column(db.String(255), nullable=True)
    
    # Store the creation date/time (UTC recommended)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # --- Foreign Key ---
    # This creates a solid link to a specific User's ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Post ID: {self.id}, Content: '{self.content[:30]}...'>"