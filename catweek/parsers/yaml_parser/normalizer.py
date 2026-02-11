from datetime import time
from .schema import WeekSchedule

def parse_time(value: str) -> tuple[time, time]:
    try:
        start_time, end_time = value.split("-")
        str_hour, str_minute = map(int, start_time.split(":"))
        end_hour, end_minute = map(int, end_time.split(":"))
        return time(str_hour, str_minute), time(end_hour, end_minute)
    except ValueError:
        raise ValueError(f"Invalid time format: {value}")

def normalize_yaml_doc(yaml_schedules: list[WeekSchedule]) -> list[dict]:
    normalized: list[dict] = []

    for schedule in yaml_schedules:
        for day, lessons in schedule.days.items():
            if not lessons:
                continue

            for lesson in lessons:

                time_start, time_end = parse_time(lesson.time)

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

    return normalized