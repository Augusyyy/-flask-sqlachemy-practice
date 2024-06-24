import uuid
from datetime import datetime
from app import db

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    name = db.Column(db.String(60), nullable=False)

    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()