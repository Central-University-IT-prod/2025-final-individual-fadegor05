from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.application.services.stats_service import (
    StatsServiceProtocol,
)
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.stats_mapper import StatsMapper
from src.presentation.rest.schemas.stats_schema import IStatsRead


class GetAdvertiserStatsUseCaseProtocol(Protocol):
    async def __call__(self, advertiser_id: UUID) -> IStatsRead: ...


class GetAdvertiserStatsUseCaseImpl:
    def __init__(
        self,
        advertiser_repository: AdvertiserRepository,
        stats_service: StatsServiceProtocol,
    ) -> None:
        self.advertiser_repository = advertiser_repository
        self.stats_service = stats_service

    async def __call__(self, advertiser_id: UUID) -> IStatsRead:
        advertiser = await self.advertiser_repository.get_by_id_or_none(advertiser_id)
        if advertiser is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        stats = await self.stats_service.get_stats_by_advertiser(advertiser)
        return StatsMapper.to_read_schema(stats)


class GetAdvertiserStatsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        advertiser_repository: AdvertiserRepository,
        stats_service: StatsServiceProtocol,
    ) -> GetAdvertiserStatsUseCaseProtocol:
        return GetAdvertiserStatsUseCaseImpl(advertiser_repository, stats_service)
