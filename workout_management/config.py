import os
from enum import Enum

basedir = os.path.abspath(os.path.dirname(__file__))


class Application(object):
    pass


class ConfigEnum(Enum):
    Production = 'production'
    Staging = 'staging'
    Development = "development"
    Testing = 'testing'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '94>,r47H8]9]Foth?RY!F4Ys^kFbZ2'
    SENDGRID_API_KEY = ''
    MAIL_FROM = "test@renanvieira.net"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@localhost:3309/workout_mgmt"
    ITEMS_PER_PAGE = 10


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@db/workout_mgmt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_IN_SECONDS = 300


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@localhost:3309/workout_mgmt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_IN_SECONDS = 300


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@localhost:3309/workout_mgmt_test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_IN_SECONDS = 2


ENVIRONMENTS = {
    ConfigEnum.Development: DevelopmentConfig(),
    ConfigEnum.Staging: StagingConfig(),
    ConfigEnum.Testing: TestingConfig(),
    ConfigEnum.Production: ProductionConfig(),
}
