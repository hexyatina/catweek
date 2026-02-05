import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
print(BASE_DIR)
yaml_path = (
    BASE_DIR
    / "catweek"
    / "data"
    / "schedules"
    / "IPZ"
    / "IPZ-3"
    / "IPZ-32.yaml"
)
print(yaml_path)

with yaml_path.open("r", encoding="utf-8") as file:
    data = yaml.safe_load_all(file)

    for doc in data:
        specialty = doc["specialty"]
        course = doc["course"]
        group_number = doc["group"]
        week_id = doc["week"]

        schedule = doc.get("schedule", {})

        print(f"{specialty}-{course}{group_number} - Неділя {week_id}")
        print(schedule)

        for day_name, lessons in schedule.items():
            if not lessons:
                continue

            print(day_name)

            for lesson in lessons:
                print(lesson)
                print(lesson["time"])
                print(lesson["lesson"])
                print(lesson["lecturer"])
                print(lesson["place"])

def parse_schedule_yaml(path: str) -> dict:
    """
    Reads YAML and returns normalized Python structure
    """