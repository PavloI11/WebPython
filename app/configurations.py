import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = b"baby"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///flaskdb.db")

class ProdConfig(Config):
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///flaskdb.db")

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///flask_testdb.db")

config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
	'test': TestConfig,
}