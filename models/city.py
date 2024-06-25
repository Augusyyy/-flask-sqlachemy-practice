import uuid
from app import db
from datetime import datetime


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    name = db.Column("name", db.String(60), nullable=False)
    country_id = db.Column("country_id", db.String(60), db.ForeignKey('countries.id'), nullable=False)
    places = db.relationship('Place', backref='city', lazy='dynamic')

    def __init__(self, name, country_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.country_id = country_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()