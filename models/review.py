import uuid
from datetime import datetime
from app import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(60), primary_key=True)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
    comment = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, user_id, place_id, comment, rating):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.place_id = place_id
        self.comment = comment
        self.rating = rating
        self.created_at = datetime.now()
        self.updated_at = datetime.now()