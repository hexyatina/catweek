from sqlalchemy import insert
from catweek.db import places, student_groups, group_presence
from catweek.db.resolvers import resolve_url, resolve_student_groups, resolve_group_presence


def insert_urls(conn, urls):
    rows = resolve_url(conn, urls)
    conn.execute(insert(places), rows)


def insert_student_groups(conn, groups):
    rows = resolve_student_groups(conn, groups)
    conn.execute(insert(student_groups), rows)


def insert_group_presence(conn, presence):
    rows = resolve_group_presence(conn, presence)
    conn.execute(insert(group_presence), rows)
