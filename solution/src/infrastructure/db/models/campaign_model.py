from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.core.enums import AllGenderEnum
from src.infrastructure.db.models.base_model import BaseModel

if TYPE_CHECKING:
    from .advertiser_model import AdvertiserModel
    from .click_model import ClickModel
    from .impression_model import ImpressionModel


class CampaignModel(BaseModel, table=True):
    cost_per_impression: Decimal = Field(
        nullable=False, max_digits=20, decimal_places=3
    )
    cost_per_click: Decimal = Field(nullable=False, max_digits=20, decimal_places=3)
    ad_title: str = Field(nullable=False)
    ad_text: str = Field(nullable=False)
    impressions_limit: int = Field(nullable=False)
    clicks_limit: int = Field(nullable=False)
    start_date: int = Field(nullable=False)
    end_date: int = Field(nullable=False)
    hide: bool = Field(nullable=False, default=False)

    gender: AllGenderEnum | None = Field(nullable=True)
    age_from: int | None = Field(nullable=True)
    age_to: int | None = Field(nullable=True)
    location: str | None = Field(nullable=True)

    image: str | None = Field(nullable=True)

    advertiser_id: UUID = Field(foreign_key="advertiser.id")
    advertiser: "AdvertiserModel" = Relationship(
        back_populates="campaigns", sa_relationship_kwargs={"lazy": "selectin"}
    )

    impressions: list["ImpressionModel"] = Relationship(
        back_populates="campaign", sa_relationship_kwargs={"lazy": "selectin"}
    )

    clicks: list["ClickModel"] = Relationship(
        back_populates="campaign", sa_relationship_kwargs={"lazy": "selectin"}
    )
