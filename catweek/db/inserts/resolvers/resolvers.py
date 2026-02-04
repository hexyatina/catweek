from sqlalchemy import select
from catweek.db import lessons, specialties, student_groups, overall_schedule






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

