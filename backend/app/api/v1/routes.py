from flask import request, jsonify, Blueprint
from sqlalchemy import text
from app import settings
from app.repositories import ScheduleRepository, LookupRepository
from app.schemas import *
from app.extensions import db


schedule_bp = Blueprint('schedule', __name__)
lookup_bp = Blueprint('lookup', __name__, url_prefix='/lookup')

system_bp = Blueprint('system', __name__)


@system_bp.route("/health", methods=["GET"])
def health():
    """
    Check the system health and database connectivity.
    ---
    tags:
      - System
    responses:
      200:
        description: System is healthy
        schema:
          properties:
            status:
              type: string
              example: ok
            database:
              type: string
              example: ok
      500:
        description: System or Database error
    """
    status = {
        "status": "ok",
        "database": "ok",
        "env": settings.ENV
    }
    try:
        db.session.execute(text("SELECT 1"), execution_options={"timeout": 5})
    except Exception as e:
        status["status"] = "error"
        status["database"] = "error"
        status["error"] = str(e)
        return jsonify(status), 500

    return jsonify(status), 200

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