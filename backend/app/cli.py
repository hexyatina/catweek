import click
from sqlalchemy import schema
from flask.cli import with_appcontext, AppGroup
from .extensions import db
from .models import *
from .data import *
from app.utils import parse_time_slot, load_and_normalize_all_yaml, IDResolver

manage_cli = AppGroup("manage", help="Database management commands.")

@manage_cli.command("seed")
@with_appcontext
def seed_db():
    """Fill database with seeded data"""
    db.session.add_all([Day(**d) for d in DAYS])
    db.session.add_all([Venue(**v) for v in VENUES])
    db.session.add_all([Lecturer(**lec) for lec in LECTURERS])
    db.session.add_all([Lesson(**l) for l in LESSONS])

    db.session.add_all([
        Slot(time_start=start_slot, time_end=end_slot)
        for start_slot, end_slot in (parse_time_slot(s_str) for s_str in SLOTS)
    ])

    spec_map = {}
    for s_data in SPECIALTIES:
        spec = Specialty(**s_data)
        db.session.add(spec)
        spec_map[s_data["code"]] = spec

    db.session.flush()

    for g_data in STUDENT_GROUPS:

        code = g_data["specialty_code"]
        if code in spec_map:
            db.session.add(StudentGroup(
                specialty_id=spec_map[code].id,
                course=g_data["course"],
                group_number=g_data["group_number"],
                )
            )
    db.session.commit()
    click.echo("Db seeded.")

@manage_cli.command("reset-content")
@with_appcontext
def reset_db():
    """Wipe all table data"""
    click.confirm("Delete ALL data?", abort=True)
    for table in reversed(Base.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    click.echo("Db reset.")

@manage_cli.command("reset-db")
@with_appcontext
def reset_db():
    """HARD RESET: Drop and recreate schema."""
    click.confirm("Drop the 'schedule' schema?", abort=True)

    target_schema = Base.metadata.schema

    with db.engine.connect() as conn:
        conn.execute(schema.DropSchema(target_schema, cascade=True, if_exists=True))
        conn.execute(schema.CreateSchema(target_schema))
        conn.commit()

    click.echo(f"Schema {target_schema} reset.")

@manage_cli.command("seed-schedule")
def seed_schedule():

    raw_rows = load_and_normalize_all_yaml("app/data/")