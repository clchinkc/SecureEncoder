import os
from decouple import config

class Config(object):
    FLASK_DEBUG = False
    FLASK_TESTING = False
    SECRET_KEY = os.urandom(24)
    FLASK_PORT = config("FLASK_PORT", default=5000, cast=int)
    ALLOWED_EXTENSIONS = {'pem'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL", default="sqlite:///md5.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    FLASK_DEBUG = False

class StagingConfig(Config):
    FLASK_DEVELOPMENT = True
    FLASK_DEBUG = True

class DevelopmentConfig(Config):
    FLASK_DEVELOPMENT = True
    FLASK_DEBUG = True

class TestingConfig(Config):
    FLASK_TESTING = True
