from pydantic import BaseModel

from src.core.fields import DateField


class ITimeCreate(BaseModel):
    current_date: DateField


class ITimeRead(ITimeCreate):
    pass
