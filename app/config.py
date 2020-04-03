import os


class Config:
    LOG_FILE_NAME = "logs/app.log"
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [ %(filename)s:%(lineno)s - %(name)s ] %(message)s "


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
