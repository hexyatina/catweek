from typing import Optional, Literal
from datetime import time as dt_time
from sqlalchemy import (
    String, Time, Index, ForeignKey, MetaData,
    CheckConstraint, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    metadata = MetaData(schema="schedule")
class Day(Base):
    __tablename__ = "days"
    id: Mapped[int] = mapped_column("day_id", primary_key=True)
    name_uk: Mapped[str] = mapped_column(String(100), unique=True)
    name_en: Mapped[str] = mapped_column(String(100), unique=True)

class Lecturer(Base):
    __tablename__ = "lecturers"
    id: Mapped[int] = mapped_column("lecturer_id", primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[Optional[str]] = mapped_column(String(100))
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))

class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column("lesson_id", primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    code: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    url: Mapped[Optional[str]] = mapped_column(String(500))

class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column("slot_id", primary_key=True)
    time_start: Mapped[dt_time] = mapped_column(Time)
    time_end: Mapped[dt_time] = mapped_column(Time)

class Venue(Base):
    __tablename__ = "venues"
    id: Mapped[int] = mapped_column("venue_id", primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

class Specialty(Base):
    __tablename__ = "specialties"
    id: Mapped[int] = mapped_column("specialty_id", primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)

class StudentGroup(Base):
    __tablename__ = "student_groups"

    id: Mapped[int] = mapped_column("group_id", primary_key=True)
    specialty_id: Mapped[int] = mapped_column(ForeignKey("specialties.specialty_id", ondelete="CASCADE"))
    course: Mapped[int]
    group_number: Mapped[int]

    __table_args__ = (
        CheckConstraint("course BETWEEN 1 AND 4", name="check_course_range"),
        UniqueConstraint("specialty_id", "course", "group_number"),
    )

class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column("schedule_id", primary_key=True)
    week_id: Mapped[int]

    day_id: Mapped[int] = mapped_column(ForeignKey("days.day_id", ondelete="CASCADE"))
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.slot_id", ondelete="CASCADE"))
    venue_id: Mapped[Optional[int]] = mapped_column(ForeignKey("venues.venue_id", ondelete="SET NULL"))
    group_id: Mapped[int] = mapped_column(ForeignKey("student_groups.group_id", ondelete="CASCADE"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.lesson_id", ondelete="CASCADE"))
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"))

    day: Mapped["Day"] = relationship()
    slot: Mapped["Slot"] = relationship()
    venue: Mapped[Optional["Venue"]] = relationship()
    group: Mapped["StudentGroup"] = relationship()
    lesson: Mapped["Lesson"] = relationship()
    lecturer: Mapped["Lecturer"] = relationship()

    __table_args__ = (
        Index("idx_group_week", "group_id", "week_id"),
        Index("idx_lecturer_week", "lecturer_id", "week_id"),
        CheckConstraint("week_id IN (1, 2)", name="check_week_id_range"),
    )
