from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship  # type: ignore

from src.infrastructure.db.models.base_model import BaseModel

if TYPE_CHECKING:
    from .campaign_model import CampaignModel
    from .ml_score_model import MLScoreModel


class AdvertiserModel(BaseModel, table=True):
    telegram_id: int | None = Field(nullable=True)
    name: str = Field(nullable=False)

    ml_scores: list["MLScoreModel"] = Relationship(
        back_populates="advertiser", sa_relationship_kwargs={"lazy": "selectin"}
    )

    campaigns: list["CampaignModel"] = Relationship(
        back_populates="advertiser", sa_relationship_kwargs={"lazy": "selectin"}
    )
