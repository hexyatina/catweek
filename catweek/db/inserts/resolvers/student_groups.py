
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