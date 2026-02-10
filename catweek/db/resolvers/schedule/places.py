from ..base import resolve_id
from catweek.db.models import places

def resolve_place_id(conn, *, place, lesson_id: int | None = None) -> int:
    if place == "online":
        where = {
            "place_type": "online",
            "lesson_id": lesson_id,
        }
        label = f"online '{lesson_id}'"
    else:
        where = {
            "place_type": "cabinet",
            "cabinet": place
        }
        label = f"cabinet '{place}'"

    return resolve_id(
        conn,
        places,
        places.c.place_id,
        where=where,
        label=label
    )