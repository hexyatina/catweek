from pathlib import Path
from sqlalchemy.exc import IntegrityError
from app.db import seed
from app.db.models import SIMPLE_TABLES, RELATIONAL_TABLES, overall_schedule
from app.services.id_resolver import IDResolver
from app.parsers.yaml_handler import load_and_normalize_yaml_doc

SEED_DATA_MAP = {
    "days": seed.DAYS,
    "times": seed.TIMES,
    "lecturers": seed.LECTURERS,
    "lessons": seed.LESSONS,
    "specialties": seed.SPECIALTIES,
}

def seed_simple_tables(conn, verbose: bool = False):

    for taget, table


def seed_from_yaml(conn, file_path):

    data = load_and_normalize_yaml_doc(file_path)

    resolver = IDResolver(conn)

    db_rows = [resolver.resolve_schedule_row(row) for row in data]

    if db_rows:
        conn.execute(overall_schedule.insert(), db_rows)
        print(f"Inserted {len(db_rows)} rows.")
    else:
        print(f"No rows found for {file_path}")

