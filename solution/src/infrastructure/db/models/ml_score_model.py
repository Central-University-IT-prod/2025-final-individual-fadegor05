from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.infrastructure.db.models.base_model import BaseModel

if TYPE_CHECKING:
    from .advertiser_model import AdvertiserModel
    from .client_model import ClientModel


class MLScoreModel(BaseModel, table=True):
    score: int = Field(nullable=False)

    client_id: UUID = Field(foreign_key="client.id")
    client: "ClientModel" = Relationship(
        back_populates="ml_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )

    advertiser_id: UUID = Field(foreign_key="advertiser.id")
    advertiser: "AdvertiserModel" = Relationship(
        back_populates="ml_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )
