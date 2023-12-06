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
    GITHUB_PAGES_URL = "https://zubeax.github.io"
    GITHUB_ACCOUNT = "zubeax"
    GITHUB_BOT_ACCOUNT = "zubeax-bot"
    GITHUB_BOT_TOKENFILE  = "./token"
    GITHUB_REPO_REMOTE = "https://{username}:{token}@github.com/{account}/{pagesrepo}"
    GITHUB_REPO_LOCAL = "./repo"
    GITHUB_COMMENT_DIRECTORY  = "_data/comments"    # this is appended to GITHUB_REPO_LOCAL

    POST_MAX_SIZE  = 2048                           # let's start with 2k
    POST_MAX_COMMENTS  = 50                         # that's 100k. Should be enough

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
