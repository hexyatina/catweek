from pathlib import Path
from temp.parsers.yaml_handler import load_and_normalize_yaml_doc
from temp.services.id_resolver import IDResolver
from app.models.schedule_tables import overall_schedule

def import_yaml_schedules(conn, data_dir: Path):

    resolver = IDResolver(conn)

    yaml_files = list(data_dir.rglob("*.yaml"))
    print(f"Found {len(yaml_files)} yaml files")

    for yaml_file in yaml_files:
        print(f"Processing {yaml_file.name}...", end=" ", flush=True)

        normalized = load_and_normalize_yaml_doc(yaml_file)

        db_rows = [resolver.resolve_schedule_row(row) for row in normalized]

        if db_rows:
            conn.execute(overall_schedule.insert(), db_rows)
            print(f"Inserted {len(db_rows)} rows.")
        else:
            print(f"No rows found for {yaml_file.name}")