from catweek.db.resolvers.schedule import resolve_specialty_id

def resolve_student_groups_seed(conn, groups: list[dict]) -> list[dict]:
    resolved = []

    for group in groups:
        specialty_id = resolve_specialty_id(conn, group["specialty_code"])

        resolved.append(
            {
                "specialty_id": specialty_id,
                "course": group["course"],
                "group_number": group["group_number"],
            }
        )

    return resolved