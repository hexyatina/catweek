from catweek.db import days, lecturers, lessons, times, places, specialties
from catweek.data import DAYS, LECTURERS, LESSONS, TIMES, CABINETS, URLS, SPECIALTIES, STUDENT_GROUPS, GROUP_PRESENCE
from .base import insert_simple, insert_urls, insert_student_groups, insert_group_presence

SIMPLE_INSERTS = [
    (days, DAYS),
    (lecturers, LECTURERS),
    (lessons, LESSONS),
    (times, TIMES),
    (places, CABINETS),
    (specialties, SPECIALTIES),
]


def insert_all_initial(conn):
    for table, rows in SIMPLE_INSERTS:
        insert_simple(conn, table, rows)

    insert_urls(conn, URLS)
    insert_student_groups(conn, STUDENT_GROUPS)
    insert_group_presence(conn, GROUP_PRESENCE)
