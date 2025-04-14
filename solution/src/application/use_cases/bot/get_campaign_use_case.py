from typing import Protocol
from uuid import UUID

from aiogram_dialog import DialogManager
from dishka import Provider, Scope, provide

from src.application.services.stats_service import StatsServiceProtocol
from src.application.services.telegram_auth_service import TelegramAuthServiceProtocol
from src.domain.repositories.campaign_repository import CampaignRepository
from src.domain.repositories.date_repository import DateRepository
from src.presentation.bot.mappers.campaign_mapper import CampaignMapper
from src.presentation.bot.schemas.campaign_schema import BCampaignRead


class GetCampaignUseCaseProtocol(Protocol):
    async def __call__(self, dialog_manager: DialogManager) -> BCampaignRead: ...


class GetCampaignUseCaseImpl:
    def __init__(
        self,
        campaign_repotisory: CampaignRepository,
        date_repository: DateRepository,
        telegram_auth_service: TelegramAuthServiceProtocol,
        stats_service: StatsServiceProtocol,
    ) -> None:
        self.campaign_repotisory = campaign_repotisory
        self.date_repository = date_repository
        self.telegram_auth_service = telegram_auth_service
        self.stats_service = stats_service

    async def __call__(self, dialog_manager: DialogManager) -> BCampaignRead:
        advertiser = await self.telegram_auth_service.auth_by_dialog_manager(
            dialog_manager
        )
        campaign_id = dialog_manager.start_data.get("campaign_id", None)
        try:
            campaign_id = UUID(campaign_id)
        except:
            raise ValueError()
        campaign = await self.campaign_repotisory.get_by_id_or_none(campaign_id)
        if campaign is None:
            raise ValueError()
        chosen_date = dialog_manager.start_data.get("chosen_date", 0)
        total_stats = await self.stats_service.get_stats_by_campaign(campaign)
        daily_stats = await self.stats_service.get_stats_daily_by_campaign(campaign)
        current_daily_stats = daily_stats[chosen_date]
        previous_daily_stats = (
            daily_stats[chosen_date - 1] if campaign.start_date != chosen_date else None
        )
        current_date = await self.date_repository.get_current_date()
        return CampaignMapper.to_read_schema(
            campaign,
            total_stats,
            current_daily_stats,
            previous_daily_stats,
            chosen_date,
            current_date,
        )


class GetCampaignUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repotisory: CampaignRepository,
        date_repository: DateRepository,
        telegram_auth_service: TelegramAuthServiceProtocol,
        stats_service: StatsServiceProtocol,
    ) -> GetCampaignUseCaseProtocol:
        return GetCampaignUseCaseImpl(
            campaign_repotisory, date_repository, telegram_auth_service, stats_service
        )
