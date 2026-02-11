import yaml
from pathlib import Path
from .schema import WeekSchedule


def load_yaml_doc(file_path: Path) -> list[WeekSchedule]:
    with file_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load_all(file)

        yaml_schedules = []

        for schedule in data:
            try:
                yaml_schedules.append(WeekSchedule(**schedule))
            except Exception as e:
                raise ValueError(f"Invalid schedule {schedule}")
    return yaml_schedules
