from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.application.services.stats_service import StatsServiceProtocol
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.stats_mapper import StatsMapper
from src.presentation.rest.schemas.stats_schema import IStatsDailyRead


class GetAdvertiserStatsDailyUseCaseProtocol(Protocol):
    async def __call__(self, advertiser_id: UUID) -> list[IStatsDailyRead]: ...


class GetAdvertiserStatsDailyUseCaseImpl:
    def __init__(
        self,
        advertiser_repository: AdvertiserRepository,
        stats_service: StatsServiceProtocol,
    ) -> None:
        self.advertiser_repository = advertiser_repository
        self.stats_service = stats_service

    async def __call__(self, advertiser_id: UUID) -> list[IStatsDailyRead]:
        advertiser = await self.advertiser_repository.get_by_id_or_none(advertiser_id)
        if advertiser is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        stats_daily = await self.stats_service.get_stats_daily_by_advertiser(advertiser)
        return [StatsMapper.to_read_schema_daily(stats) for stats in stats_daily]


class GetAdvertiserStatsDailyUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        advertiser_repository: AdvertiserRepository,
        stats_service: StatsServiceProtocol,
    ) -> GetAdvertiserStatsDailyUseCaseProtocol:
        return GetAdvertiserStatsDailyUseCaseImpl(advertiser_repository, stats_service)
