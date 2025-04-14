from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.domain.repositories.campaign_repository import CampaignRepository
from src.domain.repositories.date_repository import DateRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.campaign_mapper import CampaignMapper
from src.presentation.rest.schemas.campaign_schema import ICampaignCreate, ICampaignRead


class UpdateCampaignUseCaseProtocol(Protocol):
    async def __call__(
        self, advertiser_id: UUID, campaign_id: UUID, obj: ICampaignCreate
    ) -> ICampaignRead: ...


class UpdateCampaignUseCaseImpl:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        advertiser_repository: AdvertiserRepository,
        date_repository: DateRepository,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.advertiser_repository = advertiser_repository
        self.date_repository = date_repository

    async def __call__(
        self, advertiser_id: UUID, campaign_id: UUID, obj: ICampaignCreate
    ) -> ICampaignRead:
        advertiser = await self.advertiser_repository.get_by_id_or_none(advertiser_id)
        if advertiser is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        campaign = await self.campaign_repository.get_by_id_or_none(campaign_id)
        if campaign is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        if campaign.advertiser_id != advertiser.id:
            raise DetailedHTTPException(ExceptionEnum.NO_ACCESS)
        current_date = await self.date_repository.get_current_date()
        if current_date >= campaign.start_date:
            raise DetailedHTTPException(ExceptionEnum.VALIDATION_ERROR)
        campaign = CampaignMapper.update_domain(campaign, obj, current_date)
        if campaign is None:
            raise DetailedHTTPException(ExceptionEnum.VALIDATION_ERROR)
        campaign = await self.campaign_repository.update(campaign)
        return CampaignMapper.to_read_schema(campaign)


class UpdateCampaignUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repository: CampaignRepository,
        advertiser_repository: AdvertiserRepository,
        date_repository: DateRepository,
    ) -> UpdateCampaignUseCaseProtocol:
        return UpdateCampaignUseCaseImpl(
            campaign_repository, advertiser_repository, date_repository
        )
