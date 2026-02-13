import click
from pathlib import Path
from ..core import AppContext
from ..db.setup import init_database
from ..db.inserts.manager import execute_inserts, execute_deletes
from ..db.models import ALL_TABLES, SIMPLE_TABLES, RELATIONAL_TABLES

TABLE_CHOICES = ["all", "simple", "relational"] + list(ALL_TABLES.keys())

@click.group(name="db")
def db_group():
    """Database Manipulation (Reset, Seed, Clear)."""
    pass

@db_group.command()
@click.confirmation_option(prompt="Are you sure you want to drop the db?")
@click.pass_obj
def reset(ctx: AppContext):
    """Drop and recreate all tables (Reset)."""
    init_database(ctx)

@db_group.command()
@click.option("--target", "-t",
              type=click.Choice(TABLE_CHOICES),
              multiple=True,
              default=["all"],
              help="Group or table to seed.")
@click.pass_obj
def seed(ctx: AppContext, target):
    """Insert data (Seeded)."""

    execute_inserts(ctx, list(target), schedule_dir=Path("data/schedules"))
    click.secho(f"Seed complete for: {', '.join(target)}", fg="blue")

@click.pass_obj
@click.confirmation_option(prompt="Clear data from tables?")
def clear(ctx: AppContext, target):
    """Clear specific table."""
    execute_deletes(ctx, list(target))
    click.secho(f"Clear complete for: {', '.join(target)}", fg="yellow")

@db_group.command()
def list_tables():
    """List all tables available for manipulation."""
    click.echo("\nSimple tables:")
    for table in SIMPLE_TABLES: click.echo(f"\t{table}")
    click.echo("\nRelational tables:")
    for table in RELATIONAL_TABLES: click.echo(f"\t{table}")
    click.echo("\nschedule")
