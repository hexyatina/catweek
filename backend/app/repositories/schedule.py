from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ..models import Schedule, StudentGroup, Day, Lecturer, Specialty
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
    def get_all() -> list[Schedule]:
        stmt = ScheduleRepository._base_stmt()
        return db.session.scalars(stmt).all()

    @staticmethod
    def get_filtered(
            group: str | None = None,
            lecturer: str | None = None,
            day: str | None = None,
            week: int | None = None,
    ) -> list[Schedule]:
        stmt = ScheduleRepository._base_stmt()

        if day:
            stmt = stmt.join(Schedule.day).where(Day.name_en.ilike(f"%{day}%"))
        if lecturer:
            stmt = stmt.join(Schedule.lecturer).where(
                Lecturer.surname.ilike(f"%{lecturer}%")
            )
        if group:
            try:
                code, course, number = group.split("-")
                stmt = (stmt
                        .join(Schedule.group)
                        .join(StudentGroup.specialty)
                        .where(Specialty.code == code)
                        .where(StudentGroup.course == int(course))
                        .where(StudentGroup.group_number == int(number))
                        )
            except ValueError:
                pass
        if week:
            stmt = stmt.where(Schedule.week_id == week)

        return db.session.scalars(stmt).all()