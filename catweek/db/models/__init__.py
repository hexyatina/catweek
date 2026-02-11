from .metadata import schedule_metadata, identity_metadata
from .tables import (
    days, lessons, lecturers, times,
    places, specialties, student_groups,
    group_presence, overall_schedule
)

__all__ = [
    "schedule_metadata", "days", "lessons", "lecturers",
    "times", "places", "specialties", "student_groups",
    "group_presence", "overall_schedule", "identity_metadata"
]