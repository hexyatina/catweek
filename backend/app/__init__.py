from flask import Flask
from .extensions import db, migrate
from . import models
from .config import settings
from app.utils import init_schemas
from .cli import manage_cli

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.cli.add_command(manage_cli)

    if not app.testing:
        init_schemas(app)

    return app