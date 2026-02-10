from .schema import WeekSchedule, LessonEntry


def normalize_yaml(yaml_schedules: list[WeekSchedule]) -> list[dict]:
    normalized: list[dict] = []

    for schedule in yaml_schedules:
        for day, lessons in schedule.days.items():
            if not lessons:
                continue

            for lesson in lessons:
                normalized.append({
                    "specialty": schedule.specialty,
                    "course": schedule.course,
                    "group": schedule.group,
                    "week": schedule.week,
                    "day": day,
                    "time": lesson.time,
                    "lesson": lesson.lesson,
                    "lecturer": lesson.lecturer,
                    "place": lesson.place,
                })

    return normalized
