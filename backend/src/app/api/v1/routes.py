import logging

from flask import request, jsonify, Blueprint
from sqlalchemy import text

from src.app.repositories import ScheduleRepository, LookupRepository
from src.app.schemas import *

schedule_bp = Blueprint('schedule', __name__)
lookup_bp = Blueprint('lookup', __name__, url_prefix='/lookup')

system_bp = Blueprint('system', __name__)

logger = logging.getLogger(__name__)


@system_bp.route("/health", methods=["GET"])
def health():
    """
      Check system health and database connectivity.
      ---
      tags:
        - System
      responses:
        200:
          description: System and database are healthy
          schema:
            type: object
            properties:
              status:
                type: string
                example: ok
              database:
                type: string
                example: ok
              app_env:
                type: string
                example: prod
              db_env:
                type: string
                example: remote
        500:
          description: Database connectivity failed
          schema:
            type: object
            properties:
              status:
                type: string
                example: error
              database:
                type: string
                example: error
              app_env:
                type: string
              db_env:
                type: string
              error:
                type: string
                example: connection timeout
      """
    try:
        db.session.execute(text("SELECT 1"), execution_options={"timeout": 5})

        return jsonify({
            "status": "ok",
            "database": "ok",
            "app_env": settings.APP_ENV,
            "db_env": settings.DB_ENV,
        }), 200

    except Exception as e:
        logger.error(e)
        return jsonify({
            "status": "error",
            "database": "error",
            "app_env": settings.APP_ENV,
            "db_env": settings.DB_ENV,
            "error": str(e),
        }), 500


@schedule_bp.route("/schedule", methods=["GET"])
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
      - in: query
        name: week_id
        type: integer
        enum: [1, 2]
        required: false
      - in: query
        name: group_id
        type: integer
        example: 1
        required: false
      - in: query
        name: lecturer_id
        type: integer
        example: 1
        required: false
      - in: query
        name: detailed
        type: boolean
    responses:
      200:
        description: List of schedule entries
      401:
        description: Unauthorized
    """

    detailed = "detailed" in request.args
    filters = {
        "day_id": request.args.get("day_id", type=int),
        "week_id": request.args.get("week_id", type=int),
        "group_id": request.args.get("group_id", type=int),
        "lecturer_id": request.args.get("lecturer_id", type=int),
    }

    results = ScheduleRepository.get_filtered(**filters)
    schema = ScheduleEntryDetailSchema if detailed else ScheduleEntrySchema

    return jsonify([
        schema.from_orm_row(r).model_dump()
        for r in results
    ])


@lookup_bp.route("/days", methods=["GET"])
def get_days():
    """
    List all days
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Day list
    """
    return jsonify([
        DaySchema.model_validate(r).model_dump()
        for r in LookupRepository.get_days()
    ])


@lookup_bp.route("/slots", methods=["GET"])
def get_slots():
    """
    List all time slots
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Slot list
    """

    return jsonify([
        SlotSchema.from_orm_row(r).model_dump()
        for r in LookupRepository.get_slots()
    ])


@lookup_bp.route("/specialties", methods=["GET"])
def get_specialties():
    """
    List all specialties
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Specialty list
    """
    return jsonify([
        SpecialtySchema.model_validate(r).model_dump()
        for r in LookupRepository.get_specialties()
    ])


@lookup_bp.route("/lecturers", methods=["GET"])
def get_lecturers():
    """
    List all lecturers
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Lecturer list
    """
    return jsonify([
        LecturerSchema.model_validate(r).model_dump()
        for r in LookupRepository.get_lecturers()
    ])


@lookup_bp.route("/lessons", methods=["GET"])
def get_lessons():
    """
    List all lessons
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Lesson list
    """
    return jsonify([
        LessonSchema.model_validate(r).model_dump()
        for r in LookupRepository.get_lessons()
    ])


@lookup_bp.route("/venues", methods=["GET"])
def get_venues():
    """
    List all venues
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Venue list
    """
    return jsonify([
        VenueSchema.model_validate(r).model_dump()
        for r in LookupRepository.get_venues()
    ])


@lookup_bp.route("/groups", methods=["GET"])
def get_groups():
    """
    List all student groups
    ---
    tags:
      - Lookup
    responses:
      200:
        description: Group list
    """
    return jsonify([
        GroupSchema.from_orm_row(r).model_dump()
        for r in LookupRepository.get_groups()
    ])
