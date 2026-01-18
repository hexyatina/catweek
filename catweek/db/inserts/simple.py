from sqlalchemy import insert
from .. import days, lecturers, lessons, times, specialties

def insert_days(conn):
    conn.execute(insert(days), DAYS)

def insert_lecturers(conn):
    conn.execute(insert(lecturers), LECTURERS)


def insert_lessons(conn):
    conn.execute(insert(lessons), LESSONS)

def insert_times(conn):
    conn.execute(insert(times), TIMES)

def insert_places(conn):
    conn.execute(insert(places), PLACES)