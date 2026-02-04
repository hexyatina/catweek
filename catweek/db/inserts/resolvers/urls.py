
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