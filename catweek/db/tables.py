from sqlalchemy import (
    Table, Column, Integer, String, Time, Identity,
    ForeignKey, CheckConstraint, Boolean, UniqueConstraint, text
)
from .metadata import metadata_obj

days = Table(
    "days",
    metadata_obj,
    Column("day_id", Integer, Identity(), primary_key=True),
    Column("day_name_ua", String(100), nullable=False),
    Column("day_name_eng", String(100), nullable=False)
)

lecturers = Table(
    "lecturers",
    metadata_obj,
    Column("lecturer_id", Integer, Identity(), primary_key=True),
    Column("lecturer_name", String(100), nullable=False, unique=True)
)

lessons = Table(
    "lessons",
    metadata_obj,
    Column("lesson_id", Integer, Identity(), primary_key=True),
    Column("lesson_name", String(255), nullable=False, unique=True),
    Column("lesson_code", String(100), unique=True)
)

times = Table(
    "times",
    metadata_obj,
    Column("time_id", Integer, Identity(), primary_key=True),
    Column("time_start", Time, nullable=False),
    Column("time_end", Time, nullable=False)
)

places = Table(
    "places",
    metadata_obj,
    Column("place_id", Integer, Identity(), primary_key=True),
    Column("cabinet", String(100)),
    Column("url", String(255)),
    Column("lesson_id", Integer, ForeignKey("lessons.lesson_id", ondelete="CASCADE")),
    CheckConstraint(
        "(cabinet IS NOT NULL AND url IS NULL) OR (cabinet IS NULL AND url IS NOT NULL)",
        name="cabinet_or_url_xor"
    )
)

specialties = Table(
    "specialties",
    metadata_obj,
    Column("specialty_id", Integer, Identity(), primary_key=True),
    Column("specialty_name", String(100), nullable=False, unique=True),
    Column("specialty_code", String(10), nullable=False, unique=True)
)

student_groups = Table(
    "student_groups",
    metadata_obj,
    Column("group_id", Integer, Identity(), primary_key=True),
    Column("specialty_id", Integer, ForeignKey("specialties.specialty_id", ondelete="CASCADE")),
    Column("course", Integer, nullable=False),
    Column("group_number", Integer, nullable=False),
    CheckConstraint("course BETWEEN 1 AND 4", name="check_course_range"),
    UniqueConstraint("specialty_id", "course", "group_number")
)

group_presence = Table(
    "group_presence",
    metadata_obj,
    Column("presence_id", Integer, Identity(), primary_key=True),
    Column("group_id", Integer, ForeignKey("student_groups.group_id", ondelete="CASCADE")),
    Column("week_id", Integer, nullable=False),
    Column("is_online", Boolean, nullable=False),
    CheckConstraint("week_id IN (1, 2)", name="check_week_id_range")
)

overall_schedule = Table(
    "overall_schedule",
    metadata_obj,
    Column("schedule_id", Integer, Identity(), primary_key=True),
    Column("week_id", Integer, nullable=False),
    Column("day_id", Integer, ForeignKey("days.day_id", ondelete="CASCADE"), nullable=False),
    Column("time_id", Integer, ForeignKey("times.time_id", ondelete="CASCADE"), nullable=False),
    Column("place_id", Integer, ForeignKey("places.place_id", ondelete="CASCADE"), nullable=False),
    Column("group_id", Integer, ForeignKey("student_groups.group_id", ondelete="CASCADE"), nullable=False),
    Column("lesson_id", Integer, ForeignKey("lessons.lesson_id", ondelete="CASCADE"), nullable=False),
    Column("lecturer_id", Integer, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"), nullable=False),
    CheckConstraint("week_id IN (1, 2)", name="check_week_id_range")
)
