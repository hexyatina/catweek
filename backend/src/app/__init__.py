from flask import Flask, redirect, url_for, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from . import models as models
from .api import api_bp
from .cli import manage_cli
from .config import Settings, load_settings
from .extensions import db, migrate, swagger, talisman, cors
from .swagger_template import get_swagger_template, get_swagger_config
from .utils import configure_logging, handle_exception, handle_http_exception


def create_app(settings: Settings | None = None) -> Flask:
    cfg = settings or load_settings()

    app = Flask(__name__)

    app.config["DEBUG"] = cfg.debug
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.get_database_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["APP_ENV"] = cfg.APP_ENV
    app.config["DB_ENV"] = cfg.DB_ENV
    app.config["API_KEY"] = cfg.API_KEY
    app.config["DATABASE_URL_DIRECT"] = cfg.get_database_url(direct=True)

    app.config["APP_VERSION"] = cfg.APP_VERSION
    app.config["GIT_SHA"] = cfg.GIT_SHA

    configure_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)

    swagger.template = get_swagger_template(app)
    swagger.config = get_swagger_config()
    swagger.init_app(app)

    cors.init_app(
        app,
        resources={
            r"{}".format(cfg.CORS_API_PREFIX): {
                "origins": cfg.ALLOWED_ORIGINS,
                "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "X-Api-Key"],
                "supports_credentials": False,
            }
        },
    )

    talisman.init_app(
        app,
        force_https=cfg.FORCE_HTTPS and not cfg.debug,
        strict_transport_security=not cfg.debug,
        content_security_policy_nonce_in=[],
        x_xss_protection=False,
        content_security_policy={
            "default-src": "'self'",
            "script-src": "'self' 'unsafe-inline' 'unsafe-eval'",
            "style-src": "'self' 'unsafe-inline' fonts.googleapis.com",
            "font-src": "'self' data: fonts.gstatic.com",
            "img-src": "'self' data:",
            "connect-src": "'self'",
        },
    )

    app.cli.add_command(manage_cli)
    app.register_blueprint(api_bp)

    if cfg.debug:

        @app.route("/")
        def index():
            return redirect(url_for("flasgger.apidocs"))

    @app.route("/health")
    def health():
        """
        Liveness probe.
        """
        return jsonify(
            status="ok",
        ), 200

    @app.route("/ready")
    def ready():
        """
        Readiness probe.
        """
        checks = {"database": "ok"}

        try:
            db.session.execute(text("SELECT 1"))
        except SQLAlchemyError:
            checks["database"] = "error"
            return jsonify(status="not_ready", checks=checks), 503

        return jsonify(status="ready", checks=checks), 200

    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_exception)

    return app
