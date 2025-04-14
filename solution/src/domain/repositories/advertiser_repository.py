from typing import Self

from src.domain.entities.advertiser import AdvertiserEntity
from src.domain.repositories.base_repository import BaseRepository


class AdvertiserRepository(BaseRepository[AdvertiserEntity]):
    async def get_by_telegram_id_or_none(
        self: Self, telegram_id: int
    ) -> AdvertiserEntity | None: ...
