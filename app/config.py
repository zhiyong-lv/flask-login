import logging
import os


class Config:
    # Service Configuration
    HOSTNAME = os.environ.get('HOSTNAME', 'localhost')
    ENV = os.environ.get('FLASK_APP', 'development')

    # Log configuration
    LOG_FILE_NAME = "logs/app.log"
    LOG_FORMAT = "%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s"
    LOG_FILE_MODE = 'w'
    Log_LEVEL = logging.DEBUG

    # Database configuration
    DATABASE_DIALECT = 'mysql'
    DATABASE_DRIVER = 'pymysql'
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_NAME = 'test_flask_login'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "{DATABASE_DIALECT}+{DATABASE_DRIVER}:" \
                              "//{DATABASE_USER}:{DATABASE_PASSWORD}@" \
                              "{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?charset=utf8" \
        .format(
        DATABASE_DIALECT=DATABASE_DIALECT,
        DATABASE_DRIVER=DATABASE_DRIVER,
        DATABASE_USER=DATABASE_USER,
        DATABASE_PASSWORD=DATABASE_PASSWORD,
        DATABASE_HOST=DATABASE_HOST,
        DATABASE_PORT=DATABASE_PORT,
        DATABASE_NAME=DATABASE_NAME
    )
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', False)

    # Flask-login Configuration
    LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED', False)
    USE_SESSION_FOR_NEXT = os.environ.get('USE_SESSION_FOR_NEXT', False)
    # TODO: need ot change default value
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default for development')
    # SESSION_PROTECTION = 'strong'

    # Github Oauth Configuration
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
