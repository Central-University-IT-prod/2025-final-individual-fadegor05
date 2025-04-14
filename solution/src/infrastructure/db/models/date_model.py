from sqlmodel import Field

from src.infrastructure.db.models.base_model import BaseModel


class DateModel(BaseModel, table=True):
    date: int = Field(default=0, nullable=False)
