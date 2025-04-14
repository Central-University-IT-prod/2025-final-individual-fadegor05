from uuid import UUID

from pydantic import BaseModel

from src.core.fields import AdTextField


class IAdRead(BaseModel):
    ad_id: UUID
    ad_title: AdTextField
    ad_text: AdTextField
    ad_image: str | None = None
    advertiser_id: UUID


class IAdClickCreate(BaseModel):
    client_id: UUID
