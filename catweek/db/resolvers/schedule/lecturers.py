from catweek.db.resolvers.base import resolve_id
from catweek.db.models import lecturers

def resolve_lecturer_id(conn, lecturer_name: str) -> int:
    return resolve_id(
        conn,
        lecturers,
        lecturers.c.lecturer_id,
        where={"lecturer_name": lecturer_name},
        label=f"lecturer '{lecturer_name}'",
    )