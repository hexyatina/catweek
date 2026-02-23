from flask import Flask
from .extensions import db, migrate, swagger
from .config import settings
from .cli import manage_cli
from . import models

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    app.cli.add_command(manage_cli)

    return app