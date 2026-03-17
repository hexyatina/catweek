from pydantic import BaseModel, ConfigDict
from ..models import Slot, StudentGroup

class DaySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name_uk: str
    name_en: str


class SlotSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    time_start: int
    time_end: int
    is_short: bool

    @classmethod
    def from_orm_row(cls, r: Slot) -> "SlotSchema":
        return cls(
            id=r.id,
            time_start=r.time_start.strftime('%H:%M'),
            time_end=r.time_end.strftime('%H:%M'),
            is_short=r.is_short,
        )


class SpecialtySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str


class LecturerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    surname: str
    middle_name: str


class LessonSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    url: str | None


class VenueSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class GroupSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    specialty_name: str
    specialty_code: str
    course: int
    group_number: int

    @classmethod
    def from_orm_row(cls, r: StudentGroup) -> "GroupSchema":
        return cls(
            id=r.id,
            label=f"{r.specialty.code}-{r.course}{r.group_number}",
            specialty_name=r.specialty.name,
            specialty_code=r.specialty.code,
            course=r.course,
            group_number=r.group_number,
        )
