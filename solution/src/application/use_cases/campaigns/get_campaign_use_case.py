from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.domain.repositories.campaign_repository import CampaignRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.campaign_mapper import CampaignMapper
from src.presentation.rest.schemas.campaign_schema import ICampaignRead


class GetCampaignUseCaseProtocol(Protocol):
    async def __call__(
        self, advertiser_id: UUID, campaign_id: UUID
    ) -> ICampaignRead: ...


class GetCampaignUseCaseImpl:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        advertiser_repository: AdvertiserRepository,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.advertiser_repository = advertiser_repository

    async def __call__(self, advertiser_id: UUID, campaign_id: UUID) -> ICampaignRead:
        advertiser = await self.advertiser_repository.get_by_id_or_none(advertiser_id)
        if advertiser is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        campaign = await self.campaign_repository.get_by_id_or_none(campaign_id)
        if campaign is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        if campaign.advertiser_id != advertiser.id:
            raise DetailedHTTPException(ExceptionEnum.NO_ACCESS)
        return CampaignMapper.to_read_schema(campaign)


class GetCampaignUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repository: CampaignRepository,
        advertiser_repository: AdvertiserRepository,
    ) -> GetCampaignUseCaseProtocol:
        return GetCampaignUseCaseImpl(campaign_repository, advertiser_repository)
