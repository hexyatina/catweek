from pathlib import Path
from sqlalchemy import insert
from temp.db import seed
from app.models import SIMPLE_TABLES, RELATIONAL_TABLES, overall_schedule
from temp.services.id_resolver import IDResolver
from temp.parsers.yaml_handler import load_and_normalize_yaml_doc

def simple_seed_inserts(conn, verbose: bool = False):

    data_map = {
        "days": seed.DAYS,
        "times": seed.TIMES,
        "lecturers": seed.LECTURERS,
        "lessons": seed.LESSONS,
        "specialties": seed.SPECIALTIES,
    }

    for key, table in SIMPLE_TABLES.items():
        if verbose: print(f"  [+] Seeding table: {key}")
        conn.execute(insert(table), data_map[key])


def seed_relational(conn, verbose: bool):
    resolver = IDResolver(conn)

    with conn.begin():

        groups = [{
            "specialty_id": resolver.resolve_specialty_id(g["specialty_code"]),
            "course": g["course"],
            "group_number": g["group_number"]
        } for g in seed.STUDENT_GROUPS]
        conn.execute(insert(RELATIONAL_TABLES["student_groups"]), groups)

        # 2. Places (Mix of static data, no resolution needed)
        # Cabinets are ready to go as-is from your CABINETS list
        physical_places = seed.CABINETS

        # URLs must resolve the lesson_id first
        online_places = [{
            "place_type": "online",
            "url": u["url"],
            "lesson_id": resolver.resolve_lesson_id(u["lesson_code"]),
            "cabinet": None  # Explicitly null for online types
        } for u in seed.URLS]

        # Combine and insert
        all_places = physical_places + online_places
        conn.execute(insert(RELATIONAL_TABLES["places"]), all_places)

        # 3. Group Presence
        presence = [{
            "group_id": resolver.resolve_group_id(
                p["specialty_code"], p["course"], p["group_number"]
            ),
            "week_id": p["week_id"],
            "is_online": p["is_online"]
        } for p in seed.GROUP_PRESENCE]
        conn.execute(insert(RELATIONAL_TABLES["group_presence"]), presence)

    if verbose:
        print(f"[SUCCESS] Relational seeding complete: "
              f"{len(groups)} groups, {len(presence)} presence rules.")


def yaml_schedule_inserts(conn, schedules_dir: Path, verbose: bool = False):

    resolver = IDResolver(conn)
    yaml_files = list(schedules_dir.rglob("*.yaml"))

        for file in yaml_files:
            normalized = load_and_normalize_yaml_doc(file)
            resolved = []

            for row in normalized:
                resolved.append(resolver.resolve_schedule_row(row))

            if resolved:
                conn.execute(insert(overall_schedule), resolved)
                if verbose: print(f"  [+] Imported {file.name} ({len(resolved)} rows)")



   with conn.begin():
        for file in yaml_files:
            try:
                # Assuming this function raises an error on bad format
                normalized = load_and_normalize_yaml_doc(file)
                resolved = []

                for row in normalized:
                    # Resolve IDs (e.g., specialty_name -> specialty_id)
                    resolved.append(resolver.resolve_schedule_row(row))

                if resolved:
                    # Bulk insert for efficiency
                    conn.execute(insert(overall_schedule), resolved)

                    if verbose:
                        print(f"  [+] Imported {file.name} ({len(resolved)} rows)")

            except Exception as e:
                # Re-raise to trigger the 'with conn.begin()' rollback
                print(f"  [!] Error in {file.name}: {e}")
                raise


def insert_all(conn, schedules_dir: Path, verbose: bool = False):
    simple_seed_inserts(conn, verbose=verbose)
    relation_seed_inserts(conn, verbose=verbose)
    yaml_schedule_inserts(conn, schedules_dir, verbose=verbose)