"""Config module"""


class Config():
    """Config Vars"""
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    """Production config vars"""


class DevelopmentConfig(Config):
    """Development config vars"""
    DEBUG = True


class TestingConfig(Config):
    """Testing config vars"""
    TESTING = True
