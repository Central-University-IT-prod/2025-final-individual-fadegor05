from typing import Self

from src.domain.entities.banword import BanwordEntity
from src.domain.repositories.base_repository import BaseRepository


class BanwordRepository(BaseRepository[BanwordEntity]):
    async def get_by_word_or_none(self: Self, word: str) -> BanwordEntity | None: ...

    async def get_all_banwords_set(self) -> set[str]: ...
