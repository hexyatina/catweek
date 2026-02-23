from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from ..extensions import db
from ..models import *

class IDResolver:
    def __init__(self):
        self._cache = {}

    def _get_id(self, model, filters: dict):

        cache_key = (model.__tablename__, tuple(sorted(filters.items())))
        if cache_key in self._cache:
            return self._cache[cache_key]

        stmt = select(model.id).filter_by(**filters)
        try:
            result = db.session.execute(stmt).scalar_one()
        except NoResultFound:
            raise NoResultFound(f"Lookup failed: {model.__tablename__} with {filters}")

        self._cache[cache_key] = result
        return result

    def resolve_row(self, row:dict):

        is_en = all(ord(c) < 128 for c in row["day"])
        day_col = "name_en" if is_en else "name_uk"
        day_id = self._get_id(Day, {day_col: row["day"]})

        slot_id = self._get_id(Slot, {
            "time_start": row["time_start"],
            "time_end": row["time_end"],
        })

        venue_id = None
        if row["place"] != "online":
            venue_id = self._get_id(Venue, {"name": row["place"]})

        spec_id = self._get_id(Specialty, {"code": row["specialty"]})

        group_id = self._get_id(StudentGroup, {
            "specialty_id": spec_id,
            "course": row["course"],
            "group_number": row["group"]
        })

        lesson_id = self._get_id(Lesson, {"code": row["lesson"]})
        lecturer_id = self._get_id(Lecturer, {"surname": row["lecturer"]})

        return {
            "week_id": row["week"],
            "day_id": day_id,
            "slot_id": slot_id,
            "venue_id": venue_id,
            "group_id": group_id,
            "lesson_id": lesson_id,
            "lecturer_id": lecturer_id,
        }