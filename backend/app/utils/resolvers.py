from sqlalchemy import select, MetaData, Table
from sqlalchemy.exc import NoResultFound
from ..extensions import db
from .. import *

class IDResolver:
    def __init__(self):
        self._cache = {}

    def _get_id(self, table_name, filters):

        cache_key = (table_name, tuple(sorted(filters.items())))

        if table_name in self._cache:
            return self._cache[cache_key]

        table = self.tables[table_name]
        stmt = select(table.c[f"{table_name[:-1]}_id"])
        for col, val in filters.items():
            stmt = stmt.where(table.c[col] == val)

        res = self.conn.execute(stmt).scalar_one()
        if res is None:
            raise NoResultFound(f"No result found for {table_name} with filters {filters}")

        self._cache[cache_key] = res
        return res

    def resolve_row(self, row:dict):

        spec_id = self._get_id("specialties", {"code": row["specialty"]})
        group_id = self._get_id("groups", {
            "specialty_id": spec_id,
            "course": row["course"],
            "group_number": row["group"]
        })

        is_en = all(ord(c) < 128 for c in row["day"])
        day_col = "name_en" if is_en else "name_uk"

        return {
            "week_id": row["week_id"],
            "day_id": self._get_id("days", {day_col: row["day"]}),
            "slot_id": self._get_id("slots", {"time_start": row["time_start"], "time_end": row["time_end"]}),
            "venue_id": self._get_id("venues", {"name": row["place"]}) if row["place"] != "online" else None,
            "group_id": group_id,
            "lesson_id": self._get_id("lessons", {"name": row["lesson"]}),
            "lecturer_id": self._get_id("lecturers", {"surname": row["lecturer"]}),
        }