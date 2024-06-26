import uuid
from datetime import datetime
from app import db

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(60), primary_key=True)
    host_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.String(60), db.ForeignKey('cities.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True, default='')
    address = db.Column(db.String(1024), nullable=True, default='')
    latitude = db.Column(db.Float, nullable=True, default=None)
    longitude = db.Column(db.Float, nullable=True, default=None)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    reviews = db.relationship('Review', backref='place', lazy='dynamic')
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, host_id, city_id, name, number_of_rooms, number_of_bathrooms, price_per_night, max_guests, description='', address='', latitude=None, longitude=None):
        self.id = str(uuid.uuid4())
        self.host_id = host_id
        self.city_id = city_id
        self.name = name
        self.description = description
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.created_at = datetime.now()
        self.updated_at = datetime.now()