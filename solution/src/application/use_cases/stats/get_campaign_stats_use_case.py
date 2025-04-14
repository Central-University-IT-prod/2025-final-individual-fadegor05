from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.application.services.stats_service import (
    StatsServiceProtocol,
)
from src.domain.repositories.campaign_repository import CampaignRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.stats_mapper import StatsMapper
from src.presentation.rest.schemas.stats_schema import IStatsRead


class GetCampaignStatsUseCaseProtocol(Protocol):
    async def __call__(self, campaign_id: UUID) -> IStatsRead: ...


class GetCampaignStatsUseCaseImpl:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        stats_service: StatsServiceProtocol,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.stats_service = stats_service

    async def __call__(self, campaign_id: UUID) -> IStatsRead:
        campaign = await self.campaign_repository.get_by_id_or_none(campaign_id)
        if campaign is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        stats = await self.stats_service.get_stats_by_campaign(campaign)
        return StatsMapper.to_read_schema(stats)


class GetCampaignStatsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repository: CampaignRepository,
        stats_service: StatsServiceProtocol,
    ) -> GetCampaignStatsUseCaseProtocol:
        return GetCampaignStatsUseCaseImpl(campaign_repository, stats_service)
