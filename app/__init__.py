import logging

from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
cache = Cache()


def init_logger(config):
    if config.FLASK_ENV != 'test':
        logging.basicConfig(
            filename=config.LOG_FILE_NAME,
            format=config.LOG_FORMAT,
            filemode=config.LOG_FILE_MODE,
            level=config.Log_LEVEL
        )
    return logging.getLogger(__name__)


def create_app() -> Flask:
    '''Initalial application'''
    config = Config()
    logger = init_logger(config)

    app = Flask(__name__)
    app.config.from_object(config)

    cache.init_app(app)

    db.init_app(app)

    # Flask-SQLAlchemy must be initialized before Flask-Marshmallow.
    logger.debug("start init marshmallow")
    ma.init_app(app)

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
