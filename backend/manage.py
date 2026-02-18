import typer
from pathlib import Path
from app.core.context import AppContext
from app.scripts.import_schedules import import_yaml_schedules

cli = typer.Typer()

@cli.command()
def build(remote: bool = False):

    ctx = AppContext.create(remote_database=remote)

    with ctx.engine.begin() as conn:

        print("--- Step 1: Setting up schema and static seed ---")
