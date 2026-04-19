import hmac
import logging

from flask import request, jsonify

from ..config import settings

logger = logging.getLogger(__name__)

EXEMPT_PREFIXES = {"/", "/apidocs", "/apispec", "/flasgger_static"}


def require_api_key():
    if any(request.path == p or request.path.startswith(p) for p in EXEMPT_PREFIXES):
        return None

    key = request.headers.get("X-Api-Key", "")

    if not key:
        response = jsonify({
            "error": "Bad request",
            "message": "Missing X-Api-Key"
        })
        response.status_code = 400
        return response

    if not hmac.compare_digest(key, settings.API_KEY):
        response = jsonify({"error": "Unauthorized"})
        response.headers["WWW-Authenticate"] = 'ApiKey realm="api"'
        response.status_code = 401
        return response
    return None


def handle_http_exception(e):
    """Handles Flask/Werkzeug HTTP errors"""
    return jsonify({"error": e.description}), e.code


def handle_exception(e):
    """Catches all unhandled exceptions"""
    logger.exception(e)
    return jsonify({"error": "Internal Server Error"}), 500
