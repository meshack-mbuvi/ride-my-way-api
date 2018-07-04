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
    os.environ["DATABASE_NAME"] = "ridemyway"
    os.environ["USER"] = "ridemyway"
    os.environ["PASSWORD"] = "ridemyway"
    os.environ["HOST"] = "localhost"
    


class ProductionConfig(Config):
    DEBUG = False
    os.environ["DATABASE_NAME"] = "du15ldvvdve7g"
    os.environ["USER"] = "fykazngytmidee"
    os.environ["PASSWORD"] = "7a940a85b94644e69d871928b9dc8a7b1dda264fcfb4724ca6c0f423514b230b"
    os.environ["HOST"] = "localhost:{}".format(int(os.environ.get("PORT", 5432)))


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    os.environ["DATABASE_NAME"] = "du15ldvvdve7g"
    os.environ["USER"] = "fykazngytmidee"
    os.environ["PASSWORD"] = "7a940a85b94644e69d871928b9dc8a7b1dda264fcfb4724ca6c0f423514b230b"
    os.environ["HOST"] = "ec2-54-225-230-142.compute-1.amazonaws.com"


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
    'default': Config,
    'production': ProductionConfig
}
