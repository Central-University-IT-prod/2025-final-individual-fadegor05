from typing import Generic, Protocol, Self, TypeVar
from uuid import UUID

from src.core.pagination import Pagination
from src.domain.base import BaseDomain

BaseIDType = TypeVar("BaseIDType", bound=BaseDomain)


class BaseRepository(Protocol, Generic[BaseIDType]):
    async def get_by_id_or_none(self: Self, id: UUID) -> BaseIDType | None: ...

    async def get_paginated(self: Self, pagination: Pagination) -> list[BaseIDType]: ...

    async def create(self: Self, obj: BaseIDType) -> BaseIDType: ...

    async def bulk_create(
        self: Self, objs: list[BaseIDType]
    ) -> list[BaseIDType] | None: ...

    async def update(self: Self, obj: BaseIDType) -> BaseIDType: ...

    async def bulk_update(self: Self, objs: list[BaseIDType]) -> list[BaseIDType]: ...

    async def delete(self: Self, id: UUID) -> None: ...
