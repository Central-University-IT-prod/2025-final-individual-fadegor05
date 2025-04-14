from typing import Self, TypeVar
from uuid import UUID

from src.domain.base import BaseDomain
from src.domain.repositories.base_repository import BaseRepository

EventType = TypeVar("EventType", bound=BaseDomain)


class EventRepository(BaseRepository[EventType]):
    async def get_all_by_campaign_id(
        self: Self, campaign_id: UUID
    ) -> list[EventType]: ...

    async def get_all_by_campaign_id_and_date(
        self: Self, campaign_id: UUID, date: int
    ) -> list[EventType]: ...

    async def get_all_by_advertiser_id(
        self: Self, advertiser_id: UUID
    ) -> list[EventType]: ...

    async def get_all_by_advertiser_id_and_date(
        self: Self, advertiser_id: UUID, date: int
    ) -> list[EventType]: ...

    async def get_by_campaign_id_and_client_id_or_none(
        self: Self, campaign_id: UUID, client_id: UUID
    ) -> EventType | None: ...

    async def get_amount_by_campaign_id(self: Self, campaign_id: UUID) -> int: ...

    async def get_by_campaign_ids_and_client_id(
        self: Self, campaign_ids: list[UUID], client_id: UUID
    ) -> list[EventType]: ...

    async def get_amount_by_campaign_ids(
        self: Self, campaign_ids: list[UUID]
    ) -> dict[UUID, int]: ...
