from flask import Blueprint
from .routes import schedule_bp, lookup_bp

v1_bp = Blueprint("v1", __name__, url_prefix="/v1")

v1_bp.register_blueprint(schedule_bp)
v1_bp.register_blueprint(lookup_bp)