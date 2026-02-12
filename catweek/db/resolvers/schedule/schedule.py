from .day import resolve_day_id
from .lecturers import resolve_lecturer_id
from .lessons import resolve_lesson_id
from .places import resolve_place_id
from .student_groups import resolve_student_group_id
from .times import resolve_time_id

def resolve_schedule(conn, normalized_rows: list[dict], verbose: bool = False) -> list[dict]:
    resolved = []
    total = len(normalized_rows)

    for i, row in enumerate(normalized_rows, 1):
        lesson_id = resolve_lesson_id(conn, row["lesson"])

        resolved.append({
            "week_id": row["week"],
            "day_id": resolve_day_id(conn, row["day"]),
            "time_id": resolve_time_id(conn, time_start=row["time_start"], time_end=row["time_end"]),
            "place_id": resolve_place_id(conn, place=row["place"], lesson_id=lesson_id),
            "group_id": resolve_student_group_id(conn, specialty=row["specialty"], course=row["course"], group=row["group"]),
            "lesson_id": lesson_id,
            "lecturer_id": resolve_lecturer_id(conn, row["lecturer"])
        })

        if verbose and i % 5 == 0:
            print(f"Progress: [{i}/{total}] {row}")

    return resolved