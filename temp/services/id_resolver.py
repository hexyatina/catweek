from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from app.models.schedule_tables import days, lecturers, lessons, places, specialties, student_groups, times


class IDResolver:
    def __init__(self, conn):
        self.conn = conn
        self._cache = {}

    def _resolve(self, table, id_column, where: dict, label: str):
        cache_key = (table.name, tuple(sorted(where.items())))
        if cache_key in self._cache:
            return self._cache[cache_key]

        stmt = select(id_column).where(
            *(getattr(table.c, col) == val for col, val in where.items())
        )
        try:
            val = self.conn.execute(stmt).scalar_one()
            self._cache[cache_key] = val
            return val
        except NoResultFound:
            raise NoResultFound(f"Lookup Failed: {label} not found with criteria {where}")
        except MultipleResultsFound:
            raise MultipleResultsFound(f"Integrity Error: Multiple records for {label}")

    def resolve_day_id(self, day_name: str) -> int:
        col = "day_name_eng" if all("a" <= c.lower() <= "z" for c in day_name) else "day_name_ua"
        return self._resolve(
            days,
            days.c.day_id,
            where={col: day_name},
            label=f"day {day_name}"
        )

    def resolve_lecturer_id(self, name: str) -> int:
        return self._resolve(
            lecturers,
            lecturers.c.lecturer_id,
            where={"lecturer_name": name},
            label=f"lecturer {name}"
        )

    def resolve_lesson_id(self, lesson_name: str) -> int:
        return self._resolve(
            lessons,
            lessons.c.lesson_id,
            where={"lesson_name": lesson_name},
            label=f"lesson {lesson_name}"
        )
    def resolve_place_id(self, place: str, lesson_id: int = None) -> int:
        if place == "online":
            where = {
                "place_type": "online",
                "lesson_id": lesson_id,
            }
            label = f"online '{lesson_id}'"
        else:
            where = {
                "place_type": "cabinet",
                "cabinet": place
            }
            label = f"cabinet '{place}'"
        return self._resolve(
            places,
            places.c.place_id,
            where=where,
            label=label
        )

    def resolve_specialty_id(self, specialty_name: str) -> int:
        return self._resolve(
            specialties,
            specialties.c.specialty_id,
            where={"specialty_name": specialty_name},
            label=f"specialty '{specialty_name}'",
        )

    def resolve_student_group_id(self, specialty: str, course: int, group: int) -> int:
        specialty_id = self.resolve_specialty_id(specialty)
        where = {
            "specialty_id": specialty_id,
            "course": course,
            "group_number": group,
        }
        label = f"group {specialty}-{course}{group}"
        return self._resolve(
            student_groups,
            student_groups.c.group_id,
            where=where,
            label=label
        )

    def resolve_time_id(self, time_start, time_end) -> int:
        return self._resolve(
            times,
            times.c.times_id,
            where={
                "time_start": time_start,
                "time_end": time_end
            },
            label=f"start '{time_start}' and end '{time_end}'",
        )

    def resolve_schedule_row(self, row: dict) -> dict:

        lesson_id = self.resolve_lesson_id(row["lesson"])

        return {
            "week_id": row["week"],
            "day_id": self.resolve_day_id(row["day"]),
            "time_id": self.resolve_time_id(time_start=row["time_start"], time_end=row["time_end"]),
            "place_id": self.resolve_place_id(place=row["place"], lesson_id=lesson_id),
            "group_id": self.resolve_student_group_id(specialty=row["specialty"], course=row["course"], group=row["group"]),
            "lesson_id": lesson_id,
            "lecturer_id": self.resolve_lecturer_id(row["lecturer"])
        }