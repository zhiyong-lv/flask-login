from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)

    from .views import api
    api.init_app(app)

    from .models import User

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)

    Migrate(app, db)

    return app
