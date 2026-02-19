from flask import Flask
from .extensions import db, migrate
from .models import Base
from .config import settings
from .utils import init_schemas

def create_app():

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL

    db.init_app(app)
    init_schemas(app)
    migrate.init_app(app, db)

    return app