from uuid import UUID

from pydantic import BaseModel

from src.core.fields import NameField


class IAdvertiserRead(BaseModel):
    advertiser_id: UUID
    name: NameField
