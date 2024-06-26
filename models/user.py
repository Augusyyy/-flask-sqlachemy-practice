import uuid
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    places = db.relationship('Place', backref='host', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password