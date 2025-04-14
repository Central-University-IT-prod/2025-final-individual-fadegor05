from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.application.services.stats_service import StatsServiceProtocol
from src.domain.repositories.campaign_repository import CampaignRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.stats_mapper import StatsMapper
from src.presentation.rest.schemas.stats_schema import IStatsDailyRead


class GetCampaignStatsDailyUseCaseProtocol(Protocol):
    async def __call__(self, campaign_id: UUID) -> list[IStatsDailyRead]: ...


class GetCampaignStatsDailyUseCaseImpl:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        stats_service: StatsServiceProtocol,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.stats_service = stats_service

    async def __call__(self, campaign_id: UUID) -> list[IStatsDailyRead]:
        campaign = await self.campaign_repository.get_by_id_or_none(campaign_id)
        if campaign is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        stats_daily = await self.stats_service.get_stats_daily_by_campaign(campaign)
        return [StatsMapper.to_read_schema_daily(stats) for stats in stats_daily]


class GetCampaignStatsDailyUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repository: CampaignRepository,
        stats_service: StatsServiceProtocol,
    ) -> GetCampaignStatsDailyUseCaseProtocol:
        return GetCampaignStatsDailyUseCaseImpl(campaign_repository, stats_service)
