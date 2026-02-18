from sqlalchemy.exc import IntegrityError
from app.db import seed
from backend.app.db.models import RELATIONAL_TABLES

SEED_RESOLVER_MAP = {
    "places": lambda conn: resolve_url_seed(conn, seed.URLS) + seed.CABINETS,
    "student_groups": lambda conn: resolve_student_groups_seed(conn, seed.STUDENT_GROUPS),
    "group_presence": lambda conn: resolve_group_presence_seed(conn, seed.GROUP_PRESENCE),
}

def run_relations_insert(conn, target: str, verbose: bool = False):

    table = RELATIONAL_TABLES[target]
    resolved_data = SEED_RESOLVER_MAP[target](conn)

    try:
        conn.execute(table.insert(), resolved_data)
        if verbose:
            print(f"  [Relations] {target}: +{len(resolved_data)} rows.")
    except IntegrityError as e:
        raise RuntimeError(f"Failed to insert relational data for {target}: {e}")