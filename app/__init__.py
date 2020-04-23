import logging

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache()


def init_logger(config):
    logging.basicConfig(
        filename=config.LOG_FILE_NAME,
        format=config.LOG_FORMAT,
        filemode=config.LOG_FILE_MODE,
        level=config.Log_LEVEL
    )


def create_app():
    '''Initalial application'''
    config = Config()
    init_logger(config)

    app = Flask(__name__)
    app.config.from_object(config)

    cache.init_app(app)

    db.init_app(app)

    # TODO: CSRF, XSS, JSON

    from .views import api
    api.init_app(app)

    @app.shell_context_processor
    def make_shell_context():
        from .models import User, Document
        return dict(db=db, User=User, Document=Document)

    Migrate(app, db)
    login_manager.init_app(app)

    return app
