import os


class Config:
    LOG_FILE_NAME = "logs/app.log"
    # LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [ %(filename)s:%(lineno)s - %(name)s ] %(message)s "

    # ^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3})\s-\s(\S*)\s-\s(\S*)\s-\s(\S*)\s-\s(\S*)\s(.*)$
    # LOG_FORMAT = "%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FORMAT = "%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s"
    # LOG_FORMAT = "%(asctime)s %(name)-30s %(levelname)-8s %(message)s"
    LOG_FILE_MODE = 'w'


    DATABASE_DIALECT = 'mysql'
    DATABASE_DRIVER = 'pymysql'
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_NAME = 'test_flask_login'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
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
