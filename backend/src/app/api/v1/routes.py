import logging

from flask import request, jsonify, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.app.config import settings
from src.app.extensions import db
from src.app.repositories import ScheduleRepository, LookupRepository
from src.app.schemas import *
from src.app.utils import require_api_key

schedule_bp = Blueprint('schedule', __name__)
lookup_bp = Blueprint('lookup', __name__, url_prefix='/lookup')

system_bp = Blueprint('system', __name__)

logger = logging.getLogger(__name__)


@system_bp.get("/health")
def health():
    """
    Check system health and database connectivity.
    ---
    tags:
      - System
    responses:
      200:
        description: System and database are healthy
      500:
        description: Database connectivity failed
    """
    try:
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "ok",
            "database": "ok",
            "app_env": settings.APP_ENV,
            "db_env": settings.DB_ENV,
        }), 200

    except SQLAlchemyError:
        logger.exception("Health check failed")

        return jsonify({
            "status": "error",
            "database": "error",
            "app_env": settings.APP_ENV,
            "db_env": settings.DB_ENV,
        }), 500


@schedule_bp.get("/schedule")
@require_api_key
def get_schedule():
    """
    Get schedule entries
    ---
    tags:
      - Schedule
    parameters:
      - in: query
        name: day_id
        type: integer
        enum: [1, 2, 3, 4, 5, 6, 7]
        required: false
        description: Filter by day

      - in: query
        name: week_id
        type: integer
        enum: [1, 2]
        required: false
        description: Filter by week

      - in: query
        name: group_id
        type: integer
        required: false
        description: Filter by student group

      - in: query
        name: lecturer_id
        type: integer
        required: false
        description: Filter by lecturer

      - in: query
        name: detailed
        type: boolean
        required: false
        description: Return detailed schedule entries

    responses:
      200:
        description: List of schedule entries
        schema:
          type: array
          items:
            type: object
    """

    detailed = "detailed" in request.args
    filters = {
        "day_id": request.args.get("day_id", type=int),
        "week_id": request.args.get("week_id", type=int),
        "group_id": request.args.get("group_id", type=int),
        "lecturer_id": request.args.get("lecturer_id", type=int),
    }
    repo = ScheduleRepository()
    results = repo.get_filtered(**filters)
    schema = ScheduleEntryDetailSchema if detailed else ScheduleEntrySchema

    return jsonify([
        schema.from_orm_row(r).model_dump()
        for r in results
    ])


@lookup_bp.get("/days")
@require_api_key
def get_days():
    """
    List all days
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Day list
        schema:
          type: array
          items:
            type: object
    """
    repo = LookupRepository()
    days = repo.get_days()
    return jsonify([
        DaySchema.model_validate(d).model_dump()
        for d in days
    ])


@lookup_bp.get("/slots")
@require_api_key
def get_slots():
    """
    List all time slots
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Slots list
        schema:
          type: array
          items:
            type: object
    """
    repo = LookupRepository()
    slots = repo.get_slots()
    return jsonify([
        SlotSchema.from_orm_row(s).model_dump()
        for s in slots
    ])


@lookup_bp.get("/specialties")
@require_api_key
def get_specialties():
    """
    List all specialties
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Specialty list
        schema:
          type: array
          items:
            type: object
    """
    repo = LookupRepository()
    specialties = repo.get_specialties()
    return jsonify([
        SpecialtySchema.model_validate(s).model_dump()
        for s in specialties
    ])


@lookup_bp.get("/lecturers")
@require_api_key
def get_lecturers():
    """
    List all lecturers
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Lecturer list
        schema:
          type: array
          items:
            type: object
    """
    repo = LookupRepository()
    lecturers = repo.get_lecturers()
    return jsonify([
        LecturerSchema.model_validate(l).model_dump()
        for l in lecturers
    ])


@lookup_bp.get("/lessons")
@require_api_key
def get_lessons():
    """
    List all lessons
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Lesson list
        schema:
          type: array
          items:
            type: object
    """
    repo = LookupRepository()
    lessons = repo.get_lessons()
    return jsonify([
        LessonSchema.model_validate(l).model_dump()
        for l in lessons
    ])


@lookup_bp.get("/venues")
@require_api_key
def get_venues():
    """
    List all venues
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Venue list
        schema:
          type: array
          items:
            type: object
    """
    repo = LookupRepository()
    venues = repo.get_venues()
    return jsonify([
        VenueSchema.model_validate(v).model_dump()
        for v in venues
    ])


@lookup_bp.get("/groups")
@require_api_key
def get_groups():
    """
    List all student groups
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Groups list
        schema:
          type: array
          items:
            type: object
    """
    repo = LookupRepository()
    groups = repo.get_groups()
    return jsonify([
        GroupSchema.from_orm_row(g).model_dump()
        for g in groups
    ])
