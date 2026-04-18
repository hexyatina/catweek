from pathlib import Path

from sqlalchemy import delete

from ..extensions import db
from ..models import Schedule
from ..utils import load_and_normalize_all_yaml, IDResolver


# TODO: remake the commands
class ScheduleService:

    @staticmethod
    def import_schedule_yaml(file_path_str: str):

        file_path = Path(file_path_str)

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
