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
    


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    os.environ["DATABASE_NAME"] = "ridemyway"
    os.environ["USER"] = "ridemyway"
    os.environ["PASSWORD"] = "ridemyway"
    os.environ["HOST"] = "localhost"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    os.environ["DATABASE_NAME"] = "test"
    os.environ["USER"] = "ridemyway"
    os.environ["PASSWORD"] = "ridemyway"
    os.environ["HOST"] = "localhost"


configuration = {
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': Config
}
