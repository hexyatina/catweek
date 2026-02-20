import yaml
from pathlib import Path
from .time import parse_time_slot
from ..schemas.schedule import WeekSchedule
from pydantic import ValidationError

def load_and_normalize_all_yaml(data_dir: str) -> list[dict]:
    normalized: list[dict] = []
    path = Path(data_dir)

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {data_dir}")

    for file_path in path.rglob("*.yaml"):
        with file_path.open("r", encoding="utf-8") as file:

            documents = yaml.safe_load_all(file)

            for doc in documents:
                if not doc: continue

                try:
                    validated = WeekSchedule(**doc)
                except ValidationError as e:
                    raise RuntimeError(
                        f"Validation failed for {file_path.name} (Week {doc.get('week', 'unknown')}): \n{e}"
                    ) from e
                
                for day_name, lessons in validated.days.items():
                    if not lessons:
                        continue

                    for entry in lessons:

                        time_start, time_end = parse_time_slot(entry.time)

                        normalized.append({
                            "specialty": entry.specialty,
                            "course": entry.course,
                            "group": entry.group,
                            "week": entry.week,
                            "day": day_name,
                            "time_start": time_start,
                            "time_end": time_end,
                            "lesson": entry.lesson,
                            "lecturer": entry.lecturer,
                            "place": entry.place,
                        })
        raise normalized