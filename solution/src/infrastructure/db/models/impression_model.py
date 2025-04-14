from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.infrastructure.db.models.base_model import BaseModel

if TYPE_CHECKING:
    from .campaign_model import CampaignModel
    from .client_model import ClientModel


class ImpressionModel(BaseModel, table=True):
    date: int = Field(nullable=False)

    client_id: UUID = Field(foreign_key="client.id")
    client: "ClientModel" = Relationship(
        back_populates="impressions", sa_relationship_kwargs={"lazy": "selectin"}
    )

    campaign_id: UUID = Field(foreign_key="campaign.id")
    campaign: "CampaignModel" = Relationship(
        back_populates="impressions", sa_relationship_kwargs={"lazy": "selectin"}
    )

    cost: Decimal = Field(nullable=False, max_digits=20, decimal_places=3)
