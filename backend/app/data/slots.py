from datetime import time

SLOTS = [
    {"id": 1,  "time_start": time(9,  0),  "time_end": time(10, 20), "is_short": False},
    {"id": 2,  "time_start": time(10, 30), "time_end": time(11, 50), "is_short": False},
    {"id": 3,  "time_start": time(12, 10), "time_end": time(13, 30), "is_short": False},
    {"id": 4,  "time_start": time(13, 40), "time_end": time(15, 0), "is_short": False},
    {"id": 5,  "time_start": time(15, 10), "time_end": time(16, 30), "is_short": False},
    {"id": 6,  "time_start": time(9,  0),  "time_end": time(10,  0), "is_short": True},
    {"id": 7,  "time_start": time(10, 10), "time_end": time(11, 10), "is_short": True},
    {"id": 8,  "time_start": time(11, 20), "time_end": time(12, 20), "is_short": True},
    {"id": 9,  "time_start": time(12, 30), "time_end": time(13, 30), "is_short": True},
    {"id": 10, "time_start": time(13, 40), "time_end": time(14, 40), "is_short": True},
]