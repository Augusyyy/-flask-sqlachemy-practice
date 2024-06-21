import re
from datetime import datetime

from flask import request
from flask_restx import Resource, fields

from app import user_api, db
from config import Config
from modles.user import User

user_model = user_api.model('User', {
    'email': fields.String(required=True, description='Email address'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'password': fields.String(required=True, description='Password')
})


def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


@user_api.route('')
class Users(Resource):
    def get(self):
        """查询所有User Model的数据"""
        users = User.query.all()
        """获得数据库查询结果list，是数据库对象，不能直接返回，需要重新封装"""
        result = []
        for row in users:
            result.append({
                "id": row.id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "email": row.email,
                "password": row.password,
                "created_at": row.created_at.strftime(Config.datetime_format),
                "updated_at": row.updated_at.strftime(Config.datetime_format)
            })
        return result

    @user_api.doc('create a new user')
    @user_api.expect(user_model)
    @user_api.response(201, 'User created successfully')
    @user_api.response(400, 'Invalid input')
    @user_api.response(409, 'Email already exists')
    def post(self):
        """Begin检查参数合法性"""
        data = request.get_json()
        if not data.get('email') or not validate_email(data['email']):
            user_api.abort(400, message='Invalid input')
        if not data.get('first_name') or not data.get('last_name'):
            user_api.abort(400, message='Invalid input')

        users = User.query.all()
        for item in users:
            if item.email == data['email']:
                user_api.abort(409, 'Email already exists')
        """End检查参数合法性"""

        """Begin写入数据"""
        try:
            u = User(first_name=data["first_name"], last_name=data["last_name"], email=data["email"],
                     password=data["password"])
            db.session.add(u)
            """最后一行 db.session.commit() 很重要，只有调用了这一行才会真正把记录提交进数据库，
            前面的 db.session.add() 调用是将改动添加进数据库会话（一个临时区域）中。"""
            db.session.commit()
            return 'User created successfully', 201
        except Exception as e:
            """加入数据库commit提交失败，必须回滚"""
            db.session.rollback()
            user_api.abort(404, message='Create fail')
        """End写入数据"""


@user_api.route('/<string:user_id>')
@user_api.param('user_id', 'The user identifier')
class UserParam(Resource):
    @user_api.doc('create user by id')
    @user_api.response(404, 'User not found')
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            user_api.abort(404, message='User not found!')
        else:
            return {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "password": user.password,
                "created_at": user.created_at.strftime(Config.datetime_format),
                "updated_at": user.updated_at.strftime(Config.datetime_format)
            }

    @user_api.doc('delete_user')
    @user_api.response(204, 'User deleted successfully')
    @user_api.response(404, 'User not found')
    def delete(self, user_id):

        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return user_api.abort(404, 'User not found')
        try:
            db.session.delete(user)
            db.session.commit()
            return "delete successfully", 200
        except Exception as e:
            db.session.rollback()
            user_api.abort(404, message='Create fail')

    @user_api.doc('update_user')
    @user_api.expect(user_model)
    @user_api.response(200, 'User updated successfully')
    @user_api.response(400, 'Invalid input')
    @user_api.response(404, 'User not found')
    @user_api.response(409, 'Email already exists')
    def put(self, user_id):
        data = request.get_json()
        if request.get_json() is None:
            user_api.bort(400, "Invalid input")

        user_list = User.query.all()
        for item in user_list:
            if item.email == data['email'] and user_id != item.id:
                user_api.abort(409, 'Email already exists')

        try:
            user = User.query.filter_by(id=user_id).first()
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.password = data['password']
            user.updated_at = datetime.now()
            db.session.commit()
            return "update successfully", 200
        except Exception as e:
            db.session.rollback()
            user_api.abort(404, message='Update fail')