import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))


load_dotenv(os.path.join(BASEDIR, '.env'))


class Config(object):
    DEBUG = False
    TESTING = False


class LocalConfig(Config):
    DEBUG = True
    DB_USER_NAME = os.getenv('LOCAL_DB_USER_NAME')
    DB_USER_PWD = os.getenv('LOCAL_DB_USER_PWD')
    DB_HOST = os.getenv('LOCAL_DB_HOST')
    DB_NAME = os.getenv('LOCAL_DB_NAME')
    DB_PORT = os.getenv('LOCAL_DB_PORT')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}'.format(
        username=DB_USER_NAME,
        password=DB_USER_PWD,
        host=DB_HOST,
        db=DB_NAME,
        port=DB_PORT
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'python-intern-key-secret'