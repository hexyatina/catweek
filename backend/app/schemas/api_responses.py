from pydantic import BaseModel, ConfigDict
from app.models import Schedule


class ScheduleEntrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day: str
    time: str
    lesson: str
    lecturer: str
    location: str | None
    url: str | None
    week: int
    group: str

    @classmethod
    def from_orm_row(cls, r: Schedule) -> "ScheduleEntrySchema":
        return cls(
            day=r.day.name_uk,
            time=f"{r.slot.time_start.strftime('%H:%M')}:{r.slot.time_end.strftime('%H:%M')}",
            lesson=r.lesson.name,
            lecturer=r.lecturer.surname,
            location=r.venue.name if r.venue else None,
            url=r.lesson.url or None,
            week=r.week_id,
            group=f"{r.group.specialty.code}-{r.group.course}{r.group.group_number}",
        )