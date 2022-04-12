import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE')
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = '127.0.0.1'
