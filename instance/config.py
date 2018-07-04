import os


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

    DATABASE_URI = "postgres://fykazngytmidee:7a940a85b94644e69d871928b9dc8a7b1dda264fcfb4724ca6c0f423514b230b@ec2-54-225-230-142.compute-1.amazonaws.com:5432/du15ldvvdve7g"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True    


configuration = {
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
