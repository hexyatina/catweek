import click
from flask import current_app
from flask.cli import with_appcontext, AppGroup
from .services import ScheduleService, DatabaseService
from .extensions import db

manage_cli = AppGroup("manage", help=""
                                     "DO NOT USE IN PROD unless you know what you are doing."
                                     "Bypasses alembic migrations."
                                     "Database management commands."
                      )

@manage_cli.command("reset-content")
@with_appcontext
def reset_content():
    """Wipe all table data"""
    click.confirm("Delete ALL data?", abort=True)
    try:
        DatabaseService.reset_content()
        click.echo("Db table contents reset successfully.")
    except Exception as e:
        db.session.rollback()
        click.secho(f"Database reset failed: {e}", fg="red")

@manage_cli.command("reset-db")
@with_appcontext
def reset_db():
    """HARD RESET: Drop and recreate schema."""
    click.confirm("HARD RESET?", abort=True)
    try:
        DatabaseService.reset_db_schema(current_app)
        click.echo(f"Database recreated successfully.")
    except Exception as e:
        click.secho(f"Database recreation failed: {e}", fg="red")

@manage_cli.command("seed")
@with_appcontext
def seed_db():
    """Fill database with seeded data"""
    try:
        DatabaseService.seed_system_data()
        click.echo("Db seeded successfully.")
    except Exception as e:
        db.session.rollback()
        click.echo(f"Database seeding failed: {e}")

@manage_cli.command("import-schedule-yaml")
@with_appcontext
def import_schedule():
    """Processes all YAMLs, cleans existing entries and inserts new ones."""
    try:
        ScheduleService.import_schedule_yaml("data/schedules")
        click.echo(f"Imported schedule successfully")
    except Exception as e:
        db.session.rollback()
        click.secho(f"Import schedule failed: {e}", fg="red")