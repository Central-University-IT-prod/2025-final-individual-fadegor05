from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.application.services.moderation_service import ModerationServiceProtocol
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.domain.repositories.campaign_repository import CampaignRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.campaign_mapper import CampaignMapper
from src.presentation.rest.schemas.campaign_schema import ICampaignCreate, ICampaignRead


class CreateCampaignUseCaseProtocol(Protocol):
    async def __call__(
        self, advertiser_id: UUID, obj: ICampaignCreate
    ) -> ICampaignRead: ...


class CreateCampaignUseCaseImpl:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        advertiser_repository: AdvertiserRepository,
        moderation_service: ModerationServiceProtocol,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.advertiser_repository = advertiser_repository
        self.moderation_service = moderation_service

    async def __call__(
        self, advertiser_id: UUID, obj: ICampaignCreate
    ) -> ICampaignRead:
        advertiser = await self.advertiser_repository.get_by_id_or_none(advertiser_id)
        if advertiser is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        campaign = CampaignMapper.to_domain(obj, advertiser_id)
        content = f"{obj.ad_title}\n{obj.ad_text}"
        moderation = await self.moderation_service.moderate_content(content)
        if not moderation:
            raise DetailedHTTPException(ExceptionEnum.VALIDATION_ERROR)
        campaign = await self.campaign_repository.create(campaign)
        return CampaignMapper.to_read_schema(campaign)


class CreateCampaignUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repository: CampaignRepository,
        advertiser_repository: AdvertiserRepository,
        moderation_service: ModerationServiceProtocol,
    ) -> CreateCampaignUseCaseProtocol:
        return CreateCampaignUseCaseImpl(
            campaign_repository, advertiser_repository, moderation_service
        )
