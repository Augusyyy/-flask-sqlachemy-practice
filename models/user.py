import uuid
from datetime import datetime
"""从api的__init__.py中导入变量db"""
from app import db


class User(db.Model):
    __tablename__ = 'users'

    """创建model与sqlalchemy映射关系"""
    id = db.Column(db.String(60), nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    first_name = db.Column("first_name", db.String(20), nullable=False)
    last_name = db.Column("last_name", db.String(20), nullable=False)
    email = db.Column("email", db.String(60), nullable=False)
    password = db.Column("password", db.String(128), nullable=False)

    """与hbnb-evolution-01相同的代码"""
    def __init__(self, first_name, last_name, email, password):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password