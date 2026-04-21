from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .base import BaseRepository
from ..models import Schedule, StudentGroup


class ScheduleRepository(BaseRepository):

    @staticmethod
    def _base_stmt():
        return select(Schedule).options(
            selectinload(Schedule.day),
            selectinload(Schedule.slot),
            selectinload(Schedule.lesson),
            selectinload(Schedule.lecturer),
            selectinload(Schedule.venue),
            selectinload(Schedule.group).selectinload(StudentGroup.specialty),
        )

    def get_filtered(
            self,
            group_id: int | None = None,
            lecturer_id: int | None = None,
            day_id: int | None = None,
            week_id: int | None = None,
    ) -> list[Schedule]:
        stmt = ScheduleRepository._base_stmt()

        if day_id is not None:
            stmt = stmt.where(Schedule.day_id == day_id)
        if lecturer_id is not None:
            stmt = stmt.where(Schedule.lecturer_id == lecturer_id)
        if group_id is not None:
            stmt = stmt.where(Schedule.group_id == group_id)
        if week_id is not None:
            stmt = stmt.where(Schedule.week_id == week_id)

        stmt = stmt.order_by(
            Schedule.week_id,
            Schedule.day_id,
            Schedule.slot_id
        )

        return self.session.scalars(stmt).all()
