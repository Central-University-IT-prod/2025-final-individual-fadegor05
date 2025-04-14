from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.core.enums import GenderEnum
from src.infrastructure.db.models.base_model import BaseModel

if TYPE_CHECKING:
    from .click_model import ClickModel
    from .impression_model import ImpressionModel
    from .ml_score_model import MLScoreModel


class ClientModel(BaseModel, table=True):
    login: str = Field(nullable=False)
    age: int = Field(nullable=False)
    location: str = Field(nullable=False)
    gender: GenderEnum = Field(nullable=False)

    ml_scores: list["MLScoreModel"] = Relationship(
        back_populates="client", sa_relationship_kwargs={"lazy": "selectin"}
    )

    clicks: list["ClickModel"] = Relationship(
        back_populates="client", sa_relationship_kwargs={"lazy": "selectin"}
    )

    impressions: list["ImpressionModel"] = Relationship(
        back_populates="client", sa_relationship_kwargs={"lazy": "selectin"}
    )
