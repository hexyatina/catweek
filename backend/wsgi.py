from pathlib import Path
from temp.core import AppContext
from temp.scripts.setup_db import create_tables_and_static_seeds
from temp.scripts.import_schedules import import_all_yamls

cli = typer.Typer()


@cli.command()
def build(remote: bool = False):
    ctx = AppContext.create(remote=remote)

    with ctx.engine.begin() as conn:
        # Step 1: Create tables and insert Days, Times, etc.
        print("--- Step 1: Setting up schema and static seeds ---")
        create_tables_and_static_seeds(conn, ctx.schedule_metadata)

        # Step 2: Import YAML files
        print("\n--- Step 2: Importing YAML schedules ---")
        data_path = Path(__file__).parent.parent / "data" / "schedules"
        import_all_yamls(conn, data_path)

    print("\nDatabase build complete!")


if __name__ == "__main__":
    cli()