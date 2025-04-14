from typing import Protocol

from aiogram_dialog import DialogManager
from dishka import Provider, Scope, provide

from src.application.services.telegram_auth_service import TelegramAuthServiceProtocol
from src.domain.repositories.campaign_repository import CampaignRepository
from src.presentation.bot.mappers.campaign_mapper import CampaignMapper
from src.presentation.bot.schemas.campaign_schema import BCampaignsRead


class GetCampaignsUseCaseProtocol(Protocol):
    async def __call__(self, dialog_manager: DialogManager) -> BCampaignsRead: ...


class GetCampaignsUseCaseImpl:
    def __init__(
        self,
        campaign_repotisory: CampaignRepository,
        telegram_auth_service: TelegramAuthServiceProtocol,
    ) -> None:
        self.campaign_repotisory = campaign_repotisory
        self.telegram_auth_service = telegram_auth_service

    async def __call__(self, dialog_manager: DialogManager) -> BCampaignsRead:
        advertiser = await self.telegram_auth_service.auth_by_dialog_manager(
            dialog_manager
        )
        campaigns = await self.campaign_repotisory.get_all_by_advertiser_id(
            advertiser.id
        )
        return BCampaignsRead(
            campaigns=[
                CampaignMapper.to_base_schema(campaign) for campaign in campaigns
            ]
        )


class GetCampaignsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repotisory: CampaignRepository,
        telegram_auth_service: TelegramAuthServiceProtocol,
    ) -> GetCampaignsUseCaseProtocol:
        return GetCampaignsUseCaseImpl(campaign_repotisory, telegram_auth_service)
