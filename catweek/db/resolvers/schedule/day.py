from ..base import is_latin, resolve_id
from catweek.db.models import days

def resolve_day_id(conn, day_name: str) -> int:
    if is_latin(day_name):
        where = {"day_name_eng": day_name}
    else:
        where = {"day_name_ua": day_name}
    return resolve_id(
        conn,
        days,
        days.c.day_id,
        where=where,
        label=f"day '{day_name}'",
    )