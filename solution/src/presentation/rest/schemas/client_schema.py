from uuid import UUID

from pydantic import BaseModel

from src.core.enums import GenderEnum
from src.core.fields import AgeField, LocationField, LoginField


class IClientRead(BaseModel):
    client_id: UUID
    login: LoginField
    age: AgeField
    location: LocationField
    gender: GenderEnum
