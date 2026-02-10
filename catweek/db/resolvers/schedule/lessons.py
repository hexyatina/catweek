from catweek.db.resolvers.base import resolve_id
from catweek.db.models import lessons

def resolve_lesson_id(conn, lesson_name: str) -> int:
    return resolve_id(
        conn,
        lessons,
        lessons.c.lesson_id,
        where={"lesson_code": lesson_name},
        label=f"lesson '{lesson_name}'",
    )