from datetime import time

def parse_time_slot(value: str) -> tuple[time, time]:
    try:
        start_time, end_time = value.split("-")

        def _to_t(s: str) -> time:
            h, m = map(int, s.split(":"))
            return time(h, m)

        return _to_t(start_time), _to_t(end_time)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid time format '{value}': {e}") from e