import uuid
from datetime import datetime
"""从api的__init__.py中导入变量db"""
from app import db
from modles.city import City


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.String(60), nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    name = db.Column("name", db.String(60), nullable=False)
    code = db.Column("code", db.String(2), nullable=False)
    cities = db.relationship(City, backref='country', lazy='dynamic')

    def __init__(self, name, code):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.name = name
        self.code = code