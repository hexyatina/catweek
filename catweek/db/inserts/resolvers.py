from sqlalchemy import select
from catweek.db import lessons, specialties, student_groups


def resolve_url(conn, urls):
    resolved = []

    for url in urls:
        lesson_id = conn.execute(
            select(lessons.c.lesson_id)
            .where(lessons.c.lesson_code == url["lesson_code"])
        ).scalar_one()

        resolved.append(
            {
                "lesson_id": lesson_id,
                "url": url["url"],
            }
        )

    return resolved

def resolve_student_groups(conn, groups):
    resolved = []

    for group in groups:
        specialty_id = conn.execute(
            select(specialties.c.specialty_id)
            .where(specialties.c.specialty_code == group["specialty_code"])
        ).scalar_one()

        resolved.append(
            {
                "specialty_id": specialty_id,
                "course": group["course"],
                "group_number": group["group_number"],
            }
        )

    return resolved

def resolve_group_presence(conn, group_presence):
    resolved = []

    for group in group_presence:
        group_id = conn.execute(
            select(student_groups.c.group_id)
            .join(specialties)
            .where(specialties.c.specialty_code == group["specialty_code"],
                   student_groups.c.group_number == group["group_number"],
                   student_groups.c.course == group["course"]
            )
        ).scalar_one()

        resolved.append(
            {
                "group_id": group_id,
                "week_id": group["week_id"],
                "is_online": group["is_online"],
            }
        )

    return resolved

