from http.client import HTTPException

from flask import Flask, redirect

from . import models
from .api import api_bp
from .cli import manage_cli
from .config import settings
from .extensions import db, migrate, swagger, logger, talisman, cors
from .utils import (
    configure_logging, require_api_key, handle_exception, handle_http_exception
)


def create_app():
    app = Flask(__name__)

    configure_logging(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.get_database_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": settings.ALLOWED_ORIGINS}})
    talisman.init_app(app,
                      force_https=not settings.debug,
                      strict_transport_security=not settings.debug,
                      content_security_policy_nonce_in=[],
                      x_xss_protection=False,
                      content_security_policy={
                          "default-src": "'self'",
                          "script-src": "'self' 'unsafe-inline' 'unsafe-eval'",
                          "style-src": "'self' 'unsafe-inline'",
                          "img-src": "'self' data:",
                          "font-src": "'self' data:",
                          "connect-src": "'self'",
                      }
                      )

    app.cli.add_command(manage_cli)
    app.register_blueprint(api_bp)

    if not settings.debug:
        app.logger.info(f"Running in PRODUCTION MODE at {settings.PORT}")
        app.before_request(require_api_key)

    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_exception)
    app.add_url_rule("/", "to_docs", lambda: redirect("/apidocs/"))

    return app
