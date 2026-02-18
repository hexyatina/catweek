from pathlib import Path
from sqlalchemy.exc import IntegrityError
from backend.app.services.schedule import resolve_schedule
from backend.app.db.models import overall_schedule

def run_schedule_imports(conn, schedules_dir: Path, verbose: bool = False):
    yaml_files = list(schedules_dir.rglob("*.yaml"))

    for file in yaml_files:
        try:
            normalized = get_normalized_yaml_doc(file, verbose=verbose)
            resolved = resolve_schedule(conn, normalized, verbose=verbose)

            if not resolved:
                if verbose:
                    print(f" Skipping {file.name}, produced no lessons.")
                continue

            conn.execute(overall_schedule.insert(), resolved)

            if verbose:
                print(f" Imported {file.name} ({len(resolved)} lessons)")

        except IntegrityError as e:
            raise RuntimeError(f"Schedule insert failed for {file.name}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error processing {file.name}: {e}")