from typing import Self
from uuid import UUID

from src.core.pagination import Pagination
from src.domain.aggregates.campaign import CampaignAggregate
from src.domain.entities.client import ClientEntity
from src.domain.repositories.base_repository import BaseRepository


class CampaignRepository(BaseRepository[CampaignAggregate]):
    async def get_paginated_by_advertiser_id(
        self: Self, pagination: Pagination, advertiser_id: UUID
    ) -> list[CampaignAggregate]: ...

    async def get_all_targeting_client(
        self: Self, client: ClientEntity, current_date: int
    ) -> list[CampaignAggregate]: ...

    async def get_all_by_advertiser_id(
        self: Self, advertiser_id: UUID
    ) -> list[CampaignAggregate]: ...

    async def hide(self: Self, campaign_id: UUID) -> None: ...

    async def get_all_with_ml_scores(
        self: Self, client_id: UUID, current_date: int
    ) -> list[tuple[CampaignAggregate, int]]: ...

    async def get_stats_by_id(
        self: Self, campaign_ids: list[UUID]
    ) -> dict[UUID, tuple[int, int]]: ...
