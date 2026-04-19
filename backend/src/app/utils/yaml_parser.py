import yaml
from pathlib import Path
from .time import parse_time_slot
from ..schemas.schedule import WeekSchedule
from pydantic import ValidationError

def load_and_normalize_all_yaml(data_dir: Path) -> list[dict]:
    normalized: list[dict] = []
    path = data_dir

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {data_dir}")

    for file_path in path.rglob("*.yaml"):
        print(f"Processing {file_path.name}...")

        with file_path.open("r", encoding="utf-8") as file:

            documents = yaml.safe_load_all(file)

            for doc in documents:
                i = 0
                if doc is None: continue

                try:
                    validated = WeekSchedule(**doc)
                except ValidationError as e:
                    raise RuntimeError(
                        f"Validation failed for {file_path.name} (Week {doc.get('week', 'unknown')}): \n{e}"
                    ) from e
                
                for day_name, lessons in validated.days.items():
                    if lessons is None:
                        continue

                    for entry in lessons:
                        i = i + 1
                        time_start, time_end = parse_time_slot(entry.time)

                        normalized.append({
                            "specialty": validated.specialty,
                            "course": validated.course,
                            "group": validated.group,
                            "week": validated.week,
                            "day": day_name,
                            "time_start": time_start,
                            "time_end": time_end,
                            "lesson": entry.lesson,
                            "lecturer": entry.lecturer,
                            "place": entry.place,
                        })
                print(f"Normalized {i} lessons from {file_path.name}")
    return normalized