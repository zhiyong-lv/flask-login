from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def init_logger(app, config):
    # logging.basicConfig(
    #     filename=config.LOG_FILE_NAME,
    #     format=config.LOG_FORMAT,
    #     filemode=config.LOG_FILE_MODE
    # )

    # email errors to the administrators
    import logging
    from logging.handlers import RotatingFileHandler
    # Formatter
    # '%(asctime)s %(levelname)s %(process)d %(thread)d '
    # '%(pathname)s %(lineno)s %(message)s'
    formatter = logging.Formatter(config.LOG_FORMAT)

    class InfoFilter(logging.Filter):
        def filter(self, record):
            """only use INFO
            筛选, 只需要 INFO 级别的log
            :param record:
            :return:
            """
            if logging.INFO <= record.levelno < logging.ERROR:
                # 已经是INFO级别了
                # 然后利用父类, 返回 1
                return super().filter(record)
            else:
                return 0

    # FileHandler Info
    file_handler_info = RotatingFileHandler(filename=config.LOG_FILE_NAME)
    file_handler_info.setFormatter(formatter)
    file_handler_info.setLevel(logging.INFO)
    info_filter = InfoFilter()
    file_handler_info.addFilter(info_filter)
    app.logger.addHandler(file_handler_info)

    # FileHandler Error
    file_handler_error = RotatingFileHandler(filename=config.LOG_FILE_NAME)
    file_handler_error.setFormatter(formatter)
    file_handler_error.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler_error)


def create_app():
    '''Initalial application'''
    config = Config()

    app = Flask(__name__)
    app.config.from_object(config)
    init_logger(app, config)

    db.init_app(app)

    # TODO: CSRF, XSS, JSON

    from .views import api
    api.init_app(app)

    @app.shell_context_processor
    def make_shell_context():
        from .models import User
        return dict(db=db, User=User)

    Migrate(app, db)
    login_manager.init_app(app)

    return app
