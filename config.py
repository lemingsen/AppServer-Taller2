"""Config module"""


class Config():
    """Config Vars"""
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mongodb+srv://appserveruser:taller2@cluste' \
                   'r0-eiqhx.mongodb.net/test?retryWrites=true'
    DATABASE_NAME = 'comprame'


class ProductionConfig(Config):
    """Production config vars"""
    DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    """Development config vars"""
    DEBUG = True


class TestingConfig(Config):
    """Testing config vars"""
    TESTING = True
