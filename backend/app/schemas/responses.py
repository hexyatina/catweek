from pydantic import BaseModel, ConfigDict
from app.models import Schedule


class ScheduleEntrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day: str
    time_start: str
    time_end: str
    lesson: str
    lecturer: str
    venue: str | None
    url: str | None
    week: int
    group: str

    @classmethod
    def from_orm_row(cls, r: Schedule) -> "ScheduleEntrySchema":
        return cls(
            day=r.day.name_uk,
            time_start=r.slot.time_start.strftime("%H:%M"),
            time_end=r.slot.time_end.strftime("%H:%M"),
            lesson=r.lesson.name,
            lecturer=r.lecturer.surname,
            venue=r.venue.name if r.venue else "online",
            url=r.lesson.url or None,
            week=r.week_id,
            group=f"{r.group.specialty.code}-{r.group.course}{r.group.group_number}",
        )

class ScheduleEntryDetailSchema(ScheduleEntrySchema):

    day_en: str
    is_short: bool
    lesson_code: str
    lecturer_name: str
    lecturer_middle_name: str
    specialty_name: str
    specialty_code: str
    course: int
    group_number: int

    @classmethod
    def from_orm_row(cls, r: Schedule) -> "ScheduleEntryDetailSchema":
        return cls(
            **ScheduleEntrySchema.from_orm_row(r).model_dump(),
            day_en=r.day.name_en,
            is_short=r.slot.is_short,
            lesson_code=r.lesson.code,
            lecturer_name=r.lecturer.name,
            lecturer_middle_name=r.lecturer.middle_name,
            specialty_name=r.group.specialty.name,
            specialty_code=r.group.specialty.code,
            course=r.group.course,
            group_number=r.group.group_number,
        )