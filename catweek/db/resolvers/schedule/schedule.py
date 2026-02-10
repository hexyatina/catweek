from catweek.db.resolvers.schedule.day import resolve_day_id
from catweek.db.resolvers.schedule.lecturers import resolve_lecturer_id
from catweek.db.resolvers.schedule.lessons import resolve_lesson_id
from catweek.db.resolvers.schedule.places import resolve_place_id
from catweek.db.resolvers.schedule.student_groups import resolve_student_group_id
from catweek.db.resolvers.schedule.times import resolve_time_id

def resolve_schedule(conn, normalized_rows: list[dict]) -> list[dict]:
    resolved = []

    for row in normalized_rows:
        student_group_id = resolve_student_group_id(
            conn,
            specialty=row["specialty"],
            course=row["course"],
            group=row["group"],
        )

        day_id = resolve_day_id(conn, row["day"])

        time_id = resolve_time_id(
            conn,
            time_start=row["time_start"],
            time_end=row["time_end"],
        )

        lesson_id = resolve_lesson_id(conn, row["lesson"])

        lecturer_id = resolve_lecturer_id(conn, row["lecturer"])

        place_id = resolve_place_id(
            conn,
            place=row["place"],
            lesson_id=lesson_id,
        )

        resolved.append(
            {
                "week_id": row["week"],
                "day_id": day_id,
                "time_id": time_id,
                "place_id": place_id,
                "group_id": student_group_id,
                "lesson_id": lesson_id,
                "lecturer_id": lecturer_id,
            }
        )

    return resolved