from .metadata import metadata_obj
from .tables import (
    days, lessons, lecturers, times,
    places, specialties, student_groups,
    group_presence, overall_schedule
)

__all__ = [
    "metadata_obj", "days", "lessons", "lecturers",
    "times", "places", "specialties", "student_groups",
    "group_presence", "overall_schedule"
]