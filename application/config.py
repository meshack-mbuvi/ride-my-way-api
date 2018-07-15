import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'You and me knows very well it is secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PASSWORD = os.getenv('APP_PASSWORD')
    HOST = os.getenv('APP_HOST')
    USER = os.getenv('APP_USER')

class ProductionConfig(Config):
    DEBUG = True
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    USER = os.getenv('USER')
    DATABASE_URL = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_NAME = os.getenv('APP_DATABASE')

class TestingConfig(Config):
    TESTING = False
    DEBUG = True
    DATABASE_NAME = os.getenv('TEST_DATABASE')


configuration = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
