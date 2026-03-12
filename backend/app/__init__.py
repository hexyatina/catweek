from flask import Flask
from .extensions import db, migrate, swagger
from .config import settings
from .cli import manage_cli
from . import models
from .api.v1.routes import bp

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = settings.DEBUG

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    app.cli.add_command(manage_cli)

    app.register_blueprint(bp)

    return app