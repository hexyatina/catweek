
def resolve_overall_schedule(conn, schedule):
    resolved = []

    group_id = resolve_student_group_id(
        conn,
        parsed["meta"]
    )

    for day in parsed["days"]:
        day_id = resolve_day_id(conn, day["day"])

        for item in day["lessons"]:
            rows.append({
                "student_group_id": group_id,
                "week": parsed["meta"]["week"],
                "day_id": day_id,
                "time_id": resolve_time(conn, item["time"]),
                "lesson_id": resolve_lesson(conn, item["lesson"]),
                "lecturer_id": resolve_lecturer(conn, item["lecturer"]),
                "place_id": resolve_place(conn, item["place"]),
            })

    return resolved