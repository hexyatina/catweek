import yaml
from pathlib import Path
from datetime import time
from app.schemas.schedule import WeekSchedule
from pydantic import ValidationError

def _parse_time(value: str) -> tuple[time, time]:
    try:
        start_time, end_time = value.split("-")

        h1, m1 = map(int, start_time.split(":"))
        h2, m2 = map(int, end_time.split(":"))
        return time(h1, m1), time(h2, m2)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid time format '{value}': {e}") from e

def load_and_normalize_yaml_doc(file_path: Path) -> list[dict]:
    normalized: list[dict] = []

    if not file_path.exists():
        raise FileNotFoundError(f"Schedule file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        documents = yaml.safe_load_all(file)

        for doc in documents:
            if not doc:
                continue

            schedule = WeekSchedule(**doc)

            try:
                for day, lessons in schedule.days.items():
                    if not lessons:
                        continue

                    for lesson in lessons:

                        time_start, time_end = _parse_time(lesson.time)

                        normalized.append({
                            "specialty": schedule.specialty,
                            "course": schedule.course,
                            "group": schedule.group,
                            "week": schedule.week,
                            "day": day,
                            "time_start": time_start,
                            "time_end": time_end,
                            "lesson": lesson.lesson,
                            "lecturer": lesson.lecturer,
                            "place": lesson.place,
                        })
            except (ValidationError, ValueError) as e:
                raise RuntimeError(f"Invalid schedule format in'{file_path}': {e}") from e