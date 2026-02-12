from ..schedule.lessons import resolve_lesson_id

def resolve_url_seed(conn, urls: list[dict]) -> list[dict]:
    resolved = []
    for url in urls:
        lesson_id = resolve_lesson_id(conn, url["lesson_code"])
        resolved.append(
            {
                "place_type": "online",
                "lesson_id": lesson_id,
                "url": url["url"],
            }
        )
    return resolved