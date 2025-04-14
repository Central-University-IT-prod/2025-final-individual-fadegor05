from typing import Self
from uuid import UUID

from src.domain.aggregates.ml_score import MLScoreAggregate
from src.domain.repositories.base_repository import BaseRepository


class MLScoreRepository(BaseRepository[MLScoreAggregate]):
    async def get_by_client_advertiser_ids(
        self: Self, client_id: UUID, advertiser_ids: list[UUID]
    ) -> list[MLScoreAggregate]: ...
