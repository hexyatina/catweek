from sqlalchemy import delete
from ..utils import load_and_normalize_all_yaml, IDResolver
from ..extensions import db
from ..models import Schedule
from pathlib import Path

class ScheduleService:

    @staticmethod
    def import_schedule_yaml(file_path: str):

        file_path = Path(file_path)

        raw_data = load_and_normalize_all_yaml(file_path)
        resolver = IDResolver()

        cleaned_scopes = set()

        for row in raw_data:
            data = resolver.resolve_row(row)
            scope = (data["group_id"], data["week_id"])

            if scope not in cleaned_scopes:
                db.session.execute(
                    delete(Schedule).where(
                        Schedule.group_id == data["group_id"],
                        Schedule.week_id == data["week_id"],
                    )
                )
                cleaned_scopes.add(scope)

            db.session.add(Schedule(**data))

        print(f"Imported {len(raw_data)} rows")
        db.session.commit()
