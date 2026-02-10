from sqlalchemy import insert
from catweek.db import overall_schedule
from catweek.db.resolvers import resolve_overall_schedule


def insert_overall_schedule(conn, schedule):
    rows = resolve_overall_schedule(conn, schedule)
    conn.execute(insert(overall_schedule), rows)
