from flask import request, jsonify, Blueprint
from app.repositories import ScheduleRepository
from app.schemas import ScheduleEntrySchema

bp = Blueprint('v1', __name__, url_prefix='/api/v1/')

@bp.route("/schedule", methods=["GET"])
def get_schedule():

    group_id = request.args.get("group_id", type=int)

    results = ScheduleRepository.get_filtered_entries(group_id=group_id)

    return jsonify([ScheduleEntrySchema.model_validate(r).model_dump() for r in results])