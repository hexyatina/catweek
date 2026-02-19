from pathlib import Path
from temp.core import AppContext
from app import models
from .simple import run_simple_insert
from .relations import run_relations_insert
from .schedule import run_schedule_imports

def _resolve_targets(targets: list[str]) -> set[str]:

    if "all" in targets:
        return set(models.ALL_TABLES.keys())

    resolved = set()

    if "simple" in targets:
        resolved.update(models.SIMPLE_TABLES.keys())

    if "relational" in targets:
        resolved.update(models.RELATIONAL_TABLES.keys())

    for t in targets:
        if t in models.SIMPLE_TABLES:
            resolved.add(t)

    return resolved

def execute_inserts(ctx: AppContext, targets: list[str], schedule_dir: Path):
    to_run = _resolve_targets(targets)

    with ctx.engine.begin() as conn:

        for label in models.SIMPLE_TABLES.keys():
            if label in to_run:
                run_simple_insert(conn, label, verbose=ctx.verbose)

        for label in models.RELATIONAL_TABLES.keys():
            if label in to_run:
                run_relations_insert(conn, label, verbose=ctx.verbose)

        if "schedule" in to_run:
            if ctx.verbose:
                print(f"  [*] Starting YAML import from {schedule_dir}...")
            run_schedule_imports(conn, schedule_dir, verbose=ctx.verbose)

def execute_deletes(ctx: AppContext, targets: list[str]):

    to_run = _resolve_targets(targets)

    DELETE_ORDER = [
        "schedule",
        "group_presence",
        "places",
        "student_groups",
        "lecturers",
        "lessons",
        "times",
        "days",
        "specialties"
    ]

    with ctx.engine.begin() as conn:
        for label in DELETE_ORDER:
            if label in to_run:
                table_obj = models.ALL_TABLES[label]
                result = conn.execute(table_obj.delete())

                if ctx.verbose:
                    print(f"  [-] Cleared: {label} ({result.rowcount} rows removed)")