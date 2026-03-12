from flask import request, jsonify, Blueprint
from app.repositories import ScheduleRepository
from app.schemas import ScheduleEntrySchema

bp = Blueprint('v1', __name__, url_prefix='/api/v1')

@bp.route("/schedule", methods=["GET"])
def get_schedule():
    day = request.args.get("day")
    week = request.args.get("week", type=int)
    group = request.args.get("group")
    lecturer = request.args.get("lecturer")

    results = ScheduleRepository.get_filtered(
        group=group,
        week=week,
        day=day,
        lecturer=lecturer
    )

    return jsonify([ScheduleEntrySchema.from_orm_row(r).model_dump() for r in results])