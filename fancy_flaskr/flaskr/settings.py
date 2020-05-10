import os
from pathlib import Path


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self, basedir):
        pass


class DevelopmentConfig(BaseConfig):

    def __init__(self, basedir):
        self.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                str(Path(basedir, 'database-dev.db').absolute())


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):

    def __init__(self, basedir):
        self.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                str(Path(basedir, 'database.db').absolute())


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
