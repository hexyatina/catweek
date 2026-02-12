from .metadata import schedule_metadata, identity_metadata
from .tables import (
    days, lessons, lecturers, times,
    places, specialties, student_groups,
    group_presence, overall_schedule
)

SIMPLE_TABLES = {
    "days": days,
    "times": times,
    "lecturers": lecturers,
    "lessons": lessons,
    "specialties": specialties,
}

RELATIONAL_TABLES = {
    "places": places,
    "student_groups": student_groups,
    "group_presence": group_presence,
}

ALL_TABLES = {**SIMPLE_TABLES, **RELATIONAL_TABLES, "schedule": overall_schedule}

__all__ = [
    "schedule_metadata", "days", "lessons", "lecturers",
    "times", "places", "specialties", "student_groups",
    "group_presence", "overall_schedule", "identity_metadata",
    "SIMPLE_TABLES", "RELATIONAL_TABLES", "ALL_TABLES"
]