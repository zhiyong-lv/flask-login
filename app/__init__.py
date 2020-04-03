import logging
import logging.handlers

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()


def init_logger(config):
    logging.basicConfig(
        filename=config.LOG_FILE_NAME,
        format=config.LOG_FORMAT,
        filemode=config.LOG_FILE_MODE
    )


def create_app():
    config = Config()
    init_logger(config)

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    from .views import api
    api.init_app(app)

    from .models import User

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)

    Migrate(app, db)

    return app
