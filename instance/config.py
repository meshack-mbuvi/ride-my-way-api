import os
from os.path import join, dirname
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = join(dirname(__file__), '.env')

# load file from the path
load_dotenv(dotenv_path)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'You and me knows very well it is secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    DATABASE_URI = os.getenv('DATABASE_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    USER = os.getenv('USER')
    


class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    DATABASE_URI = os.getenv('DATABASE_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    USER = os.getenv('USER')



class TestingConfig(Config):
    TESTING = True
    DEBUG = True    


configuration = {
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
