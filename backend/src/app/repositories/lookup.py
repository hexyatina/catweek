from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .base import BaseRepository
from ..models import Day, Slot, Specialty, Lecturer, Lesson, Venue, StudentGroup


class LookupRepository(BaseRepository):
    def get_days(self) -> list[Day]:
        return self.session.scalars(
            select(Day).order_by(Day.id)
        ).all()

    def get_slots(self) -> list[Slot]:
        return self.session.scalars(
            select(Slot).order_by(Slot.id)
        ).all()

    def get_specialties(self) -> list[Specialty]:
        return self.session.scalars(
            select(Specialty).order_by(Specialty.id)
        ).all()

    def get_lecturers(self) -> list[Lecturer]:
        return self.session.scalars(
            select(Lecturer).order_by(Lecturer.surname)
        ).all()

    def get_lessons(self) -> list[Lesson]:
        return self.session.scalars(
            select(Lesson).order_by(Lesson.name)
        ).all()

    def get_venues(self) -> list[Venue]:
        return self.session.scalars(
            select(Venue).order_by(Venue.id)
        ).all()

    def get_groups(self) -> list[StudentGroup]:
        return self.session.scalars(
            select(StudentGroup)
            .options(joinedload(StudentGroup.specialty))
            .order_by(StudentGroup.specialty_id, StudentGroup.course, StudentGroup.group_number)
        ).all()
