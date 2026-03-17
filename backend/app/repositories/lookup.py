from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ..models import Day, Slot, Specialty, Lecturer, Lesson, Venue, StudentGroup
from ..extensions import db

class LookupRepository:

    @staticmethod
    def get_days() -> list[Day]:
        return db.session.scalars(
            select(Day).order_by(Day.id)
        ).all()

    @staticmethod
    def get_slots() -> list[Slot]:
        return db.session.scalars(
            select(Slot).order_by(Slot.id)
        ).all()

    @staticmethod
    def get_specialties() -> list[Specialty]:
        return db.session.scalars(
            select(Specialty).order_by(Specialty.id)
        ).all()

    @staticmethod
    def get_lecturers() -> list[Lecturer]:
        return db.session.scalars(
            select(Lecturer).order_by(Lecturer.surname)
        ).all()

    @staticmethod
    def get_lessons() -> list[Lesson]:
        return db.session.scalars(
            select(Lesson).order_by(Lesson.name)
        ).all()

    @staticmethod
    def get_venues() -> list[Venue]:
        return db.session.scalars(
            select(Venue).order_by(Venue.id)
        ).all()

    @staticmethod
    def get_groups() -> list[StudentGroup]:
        return db.session.scalars(
            select(StudentGroup)
            .options(joinedload(StudentGroup.specialty))
            .order_by(StudentGroup.specialty_id, StudentGroup.course, StudentGroup.group_number)
        ).all()