from typing import Self

from src.domain.entities.date import DateEntity
from src.domain.repositories.base_repository import BaseRepository


class DateRepository(BaseRepository[DateEntity]):
    async def upsert_current_date(self: Self, date: int) -> int: ...

    async def get_current_date(self: Self) -> int: ...

    async def increment_current_date(self: Self) -> int: ...
