from ..utils import load_and_normalize_all_yaml, IDResolver
from ..extensions import db

def import_schedule_from_yaml(file_path):

    raw_data = load_and_normalize_all_yaml(file_path)

    resolver = IDResolver()

    for row in raw_data:
        db.session.add(resolver.resolve_row(row))

    db.session.commit()