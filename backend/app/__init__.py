from flask import Flask, request, jsonify, redirect
from .extensions import db, migrate, swagger
from .config import settings
from .cli import manage_cli
from . import models
from .api import api_bp

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = settings.DEBUG

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    app.cli.add_command(manage_cli)

    app.register_blueprint(api_bp)

    if not settings.DEBUG:
        print("\nPRODUCTION MODE IS ON\n")
        @app.before_request
        def require_api_key():
            if (
                    request.path == "/" or
                    request.path.startswith("/apidocs") or
                    request.path.startswith("/apispec") or
                    request.path.startswith("/flasgger_static")
            ):
                return None
            key = request.headers.get("X-Api-Key")
            if key != settings.API_KEY:
                return jsonify({"error": "Unauthorized"}), 401

    @app.route("/")
    def to_docs():
        return redirect("/apidocs/")

    return app