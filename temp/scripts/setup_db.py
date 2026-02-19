from sqlalchemy import insert
from app.models import (
    schedule_metadata, identity_metadata,
    SIMPLE_TABLES, RELATIONAL_TABLES
)
from temp.services.id_resolver import IDResolver


def create_tables(conn):
    print("Resetting database schema...")
    schedule_metadata.drop_all(bind=conn.engine)
    identity_metadata.drop_all(bind=conn.engine)

    schedule_metadata.create_all(bind=conn.engine)
    identity_metadata.create_all(bind=conn.engine)


def seed_simple_tables(conn, verbose: bool):
    seeds = {
        "days": days,
        "times": times.data,
        "lecturers": lecturers.data,
        "lessons": lessons.data,
        "specialties": specialties.data,
    }

    for name, table in SIMPLE_TABLES.items():
        if verbose:
            print(f"Seeding simple table: {name}...")
        conn.execute(insert(table), seeds[name])


def seed_relational_tables(conn, verbose: bool):
    """Seeds tables that require ID resolution before insertion."""
    resolver = IDResolver(conn)

    # 1. Resolve & Seed Student Groups
    if verbose: print("Resolving and seeding Student Groups...")
    resolved_groups = [
        {
            "specialty_id": resolver.resolve_specialty_id(g["specialty"]),
            "course": g["course"],
            "group_number": g["group_number"]
        }
        for g in student_groups.data
    ]
    conn.execute(insert(RELATIONAL_TABLES["student_groups"]), resolved_groups)

    # 2. Resolve & Seed Places
    if verbose: print("Resolving and seeding Places...")
    # Places usually don't need resolution unless they link to lessons
    # (e.g., online links). If they are just cabinets, insert directly.
    conn.execute(insert(RELATIONAL_TABLES["places"]), places.data)

    # 3. Resolve & Seed Group Presence
    if verbose: print("Resolving and seeding Group Presence...")
    resolved_presence = [
        {
            "group_id": resolver.resolve_group_id(p["specialty"], p["course"], p["group"]),
            "is_present": p["is_present"]
        }
        for p in group_presence.data
    ]
    conn.execute(insert(RELATIONAL_TABLES["group_presence"]), resolved_presence)


def setup_all(conn, verbose: bool):
    """Main orchestration for DB setup."""
    create_tables(conn)
    seed_simple_tables(conn, verbose)
    seed_relational_tables(conn, verbose)