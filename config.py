"""Config Vars"""
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mongodb+srv://appserveruser:taller2@cluster0-eiqhx.mongodb.net/test?retryWrites=true'


"""Production config"""
class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'


"""Development config"""
class DevelopmentConfig(Config):
    DEBUG = True


"""Testing config"""
class TestingConfig(Config):
    TESTING = True