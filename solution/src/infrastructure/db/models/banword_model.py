from sqlmodel import Field

from src.infrastructure.db.models.base_model import BaseModel


class BanwordModel(BaseModel, table=True):
    word: str = Field(nullable=False, unique=True)
