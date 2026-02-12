from sqlalchemy.exc import IntegrityError
from catweek.data import seed
from ..models import SIMPLE_TABLES

SEED_DATA_MAP = {
    "days": seed.DAYS,
    "times": seed.TIMES,
    "lecturers": seed.LECTURERS,
    "lessons": seed.LESSONS,
    "specialties": seed.SPECIALTIES,
}

def run_simple_insert(conn, target: str, verbose: bool = False):

    table = SIMPLE_TABLES[target]
    data = SEED_DATA_MAP[target]

    try:
        result = conn.execute(table.insert(), data)
        if verbose:
            print(f"  [Simple] {target}: +{result.rowcount} rows.")
    except IntegrityError as e:
        raise RuntimeError(f"Failed to insert simple data for {target}: {e}")