import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """时间格式"""
    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    # SECRET_KEY 秘钥为路径内或者 字符串 'A-VERY-LONG-SECRET' 可以随意设置，主要为了防止跨网站攻击
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:yxylfh9986@localhost:3306/hbnb_evo_db?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True