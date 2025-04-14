from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel  # type: ignore


class BaseModel(SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # type: ignore
        return cls.__name__.lower().replace("model", "")

    id: UUID = Field(
        default_factory=uuid4, primary_key=True, index=True, nullable=False
    )


class TimestampMixin:
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),  # type: ignore
        default_factory=lambda: datetime.now(),
    )
