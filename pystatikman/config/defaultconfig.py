__author__ = 'Axel Zuber'


class DefaultConfig(object):
    """
    Default Config (Is used when PYSTATIKMANCONFIG environment variable is not set)
    """
    APP_NAME = 'pystatikman'
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    LOG_DIR = 'logs/'
    SQLALCHEMY_DATABASE_URI = "sqlite:///comment.db"


class Development(DefaultConfig):
    """
    Config class for development.
    """
    DEBUG = True
    LOG_LEVEL = 'INFO'
    SQLALCHEMY_DATABASE_URI = "sqlite:///comment_test.db"


class UnitTesting(DefaultConfig):
    """
    Config class for unittests
    """
    DEBUG = True
    LOG_LEVEL = 'INFO'
    SQLALCHEMY_DATABASE_URI = "sqlite:///comment_unittest.db"