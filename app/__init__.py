from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config

"""初始化flask"""
app = Flask(__name__)
"""导入配置"""
app.config.from_object(Config)
"""初始化SQLAlchemy"""
db = SQLAlchemy(app)
"""初始化Restx"""
api = Api(app, version='1.0', title='Flask-sqlalchemy API', description='Flask-sqlalchemy project API')

"""使用namesapce继续对url进行分类扩展。127.0.0.1:5000/api/v1/users"""
user_api = api.namespace("api/v1/users", description='User operation')

country_api = api.namespace('api/v1/countries', description='Country operations')

city_api = api.namespace('api/v1/city', description='City operations')

from app.user_api import *

from app.country_api import *

from app.city_api import *