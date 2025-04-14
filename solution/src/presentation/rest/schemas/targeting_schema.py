from pydantic import BaseModel

from src.core.enums import AllGenderEnum
from src.core.fields import AgeField, LocationField


class ITargetRead(BaseModel):
    gender: AllGenderEnum | None = None
    age_from: AgeField | None = None
    age_to: AgeField | None = None
    location: LocationField | None = None
