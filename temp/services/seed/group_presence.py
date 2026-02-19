from ..schedule.student_groups import resolve_student_group_id
def resolve_group_presence_seed(conn, group_presence: list[dict]) -> list[dict]:
    resolved = []

    for group in group_presence:
        group_id = resolve_student_group_id(
            conn,
            specialty=group["specialty_code"],
            course = group["course"],
            group = group["group_number"],
        )

        resolved.append(
            {
                "group_id": group_id,
                "week_id": group["week_id"],
                "is_online": group["is_online"],
            }
        )

    return resolved