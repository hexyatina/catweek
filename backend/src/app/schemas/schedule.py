from pydantic import BaseModel, Field

class LessonEntry(BaseModel):
    time: str = Field(..., pattern=r"^\d{2}:\d{2}-\d{2}:\d{2}$")
    lesson: str
    lecturer: str
    place: str

class WeekSchedule(BaseModel):
    specialty: str
    course: int = Field(gt=0, le=4)
    group: int = Field(gt=0)
    week: int = Field(ge=1, le=2)
    days: dict[str, list[LessonEntry] | None]