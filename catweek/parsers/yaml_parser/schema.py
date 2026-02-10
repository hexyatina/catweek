from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class LessonEntry(BaseModel):
    time: str
    lesson: str
    lecturer: str
    place: str

class WeekSchedule(BaseModel):
    specialty: str
    course: int = Field(gt=0, le=4)
    group: int = Field(gt=0)
    week: int = Field(ge=1, le=2)
    days: Dict[str, Optional[List[LessonEntry]]]