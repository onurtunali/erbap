"""Application configuration.

Most configuration is set via environment variables that were loaded with `load_dotenv`. For local development, use an .env file to setenvironment variables.
"""
import os


class Config(object):
    TESTING = False
    DATABASE = os.getenv("DATABASE")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    TESTING = False


class DevelopmentConfig(Config):
    TESTING = True


class TestingConfig(Config):
    TESTING = True
