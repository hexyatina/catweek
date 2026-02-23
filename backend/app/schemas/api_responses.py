from pydantic import BaseModel, ConfigDict

class ScheduleEntrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day: str
    time: str
    lesson: str
    lecturer: str
    location: str | None
    url: str | None