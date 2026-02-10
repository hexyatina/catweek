from .specialty import resolve_specialty_id
from catweek.db.resolvers.base import resolve_id
from catweek.db.models import student_groups

def resolve_student_group_id(conn, *, specialty: str, course: int, group: int) -> int:
    specialty_id = resolve_specialty_id(conn, specialty)

    return resolve_id(
        conn,
        student_groups,
        student_groups.c.group_id,
        where={
            "specialty_id": specialty_id,
            "course": course,
            "group_number": group,
        },
        label=f"group {specialty}-{course}-{group}",
    )
