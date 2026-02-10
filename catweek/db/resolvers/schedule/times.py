from catweek.db.resolvers.base import resolve_id
from catweek.db.models import times
from datetime import time

def resolve_time_id(conn, *, time_start: time, time_end: time) -> int:
    return resolve_id(
        conn,
        times,
        times.c.time_id,
        where={
            "time_start": time_start,
            "time_end": time_end
        },
        label=f"time '{time_start}' and '{time_end}'",
    )