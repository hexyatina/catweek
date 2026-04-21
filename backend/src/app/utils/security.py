import hmac
import logging
from functools import wraps

from flask import request, jsonify

from ..config import settings

logger = logging.getLogger(__name__)


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if settings.debug:
            return f(*args, **kwargs)

        key = request.headers.get("X-Api-Key", "")

        if not key:
            return jsonify({"error": "Missing API Key"}), 401

        if not hmac.compare_digest(key, settings.API_KEY):
            return jsonify({"error": "Invalid API Key"}), 403

        return f(*args, **kwargs)

    return decorated


def handle_http_exception(e):
    """Handles Flask/Werkzeug HTTP errors"""
    return jsonify({"error": e.description}), e.code


def handle_exception(e):
    """Catches all unhandled exceptions"""
    logger.exception(e)
    return jsonify({"error": "Internal Server Error"}), 500
