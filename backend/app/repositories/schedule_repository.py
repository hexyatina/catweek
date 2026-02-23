from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ..models import Schedule
from ..extensions import db

class ScheduleRepository:
    @staticmethod
    def get_filtered_entries(week_id=None, day_id=None, slot_id=None, venue_id=None, group_id=None, lesson_id=None, lecturer_id=None):

        stmt = select(Schedule).options(
            joinedload(Schedule.day),
            joinedload(Schedule.slot),
            joinedload(Schedule.lesson),
            joinedload(Schedule.lecturer),
            joinedload(Schedule.venue),
        )

        return db.session.scalars(stmt).all()