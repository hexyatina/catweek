from .schedule import resolve_schedule
from .specialty import resolve_specialty_id
from .student_groups import resolve_student_group_id
from .lessons import resolve_lesson_id

__all__ = [
    "resolve_schedule", "resolve_lesson_id",
           "resolve_specialty_id", "resolve_student_group_id"
           ]