from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ..models import Schedule, StudentGroup
from ..extensions import db

class ScheduleRepository:

    @staticmethod
    def _base_stmt():
        return select(Schedule).options(
            joinedload(Schedule.day),
            joinedload(Schedule.slot),
            joinedload(Schedule.lesson),
            joinedload(Schedule.lecturer),
            joinedload(Schedule.venue),
            joinedload(Schedule.group).joinedload(StudentGroup.specialty),
        )

    @staticmethod
    def get_filtered(
            group_id: int | None = None,
            lecturer_id: int | None = None,
            day_id: int | None = None,
            week_id: int | None = None,
    ) -> list[Schedule]:
        stmt = ScheduleRepository._base_stmt()

        if day_id:
            stmt = stmt.where(Schedule.day_id == day_id)
        if lecturer_id:
            stmt = stmt.where(Schedule.lecturer_id == lecturer_id)
        if group_id:
            stmt = stmt.where(Schedule.group_id == group_id)
        if week_id:
            stmt = stmt.where(Schedule.week_id == week_id)

        stmt = stmt.order_by(
            Schedule.week_id.asc(),
            Schedule.day_id.asc(),
            Schedule.slot_id.asc()
        )

        return db.session.scalars(stmt).all()