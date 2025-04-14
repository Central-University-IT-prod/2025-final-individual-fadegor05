from typing import Protocol

from aiogram_dialog import DialogManager
from dishka import Provider, Scope, provide

from src.application.services.stats_service import StatsServiceProtocol
from src.application.services.telegram_auth_service import TelegramAuthServiceProtocol
from src.domain.repositories.campaign_repository import CampaignRepository
from src.domain.repositories.date_repository import DateRepository
from src.presentation.bot.mappers.advertiser_mapper import AdvertiserMapper
from src.presentation.bot.schemas.advertiser_schema import BAdvertiserStatsRead


class GetStatsUseCaseProtocol(Protocol):
    async def __call__(self, dialog_manager: DialogManager) -> BAdvertiserStatsRead: ...


class GetStatsUseCaseImpl:
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

    async def __call__(self, dialog_manager: DialogManager) -> BAdvertiserStatsRead:
        advertiser = await self.telegram_auth_service.auth_by_dialog_manager(
            dialog_manager
        )
        chosen_date = dialog_manager.start_data.get("chosen_date", 0)
        total_stats = await self.stats_service.get_stats_by_advertiser(advertiser)
        daily_stats = await self.stats_service.get_stats_daily_by_advertiser(advertiser)
        date = await self.date_repository.get_current_date()
        current_daily_stats = daily_stats[chosen_date]
        previous_daily_stats = daily_stats[chosen_date - 1] if chosen_date > 0 else None
        return AdvertiserMapper.to_read_schema(
            advertiser,
            total_stats,
            current_daily_stats,
            previous_daily_stats,
            chosen_date,
            date,
        )


class GetStatsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repotisory: CampaignRepository,
        date_repository: DateRepository,
        telegram_auth_service: TelegramAuthServiceProtocol,
        stats_service: StatsServiceProtocol,
    ) -> GetStatsUseCaseProtocol:
        return GetStatsUseCaseImpl(
            campaign_repotisory, date_repository, telegram_auth_service, stats_service
        )
