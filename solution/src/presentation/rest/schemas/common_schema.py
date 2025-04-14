from typing import TypeVar

from pydantic import BaseModel, Field

IType = TypeVar("IType")


class IPaginationCommon(BaseModel):
    size: int = Field(default=10, gt=0)
    page: int = Field(default=0, ge=0)


class IDetailedException(BaseModel):
    message: str
