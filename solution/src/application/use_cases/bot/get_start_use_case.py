from typing import Protocol

from aiogram_dialog import DialogManager
from dishka import Provider, Scope, provide

from src.application.services.stats_service import StatsServiceProtocol
from src.application.services.telegram_auth_service import TelegramAuthServiceProtocol
from src.domain.repositories.date_repository import DateRepository
from src.presentation.bot.mappers.start_mapper import StartMapper
from src.presentation.bot.schemas.start_schema import BStartRead


class GetStartUseCaseProtocol(Protocol):
    async def __call__(self, dialog_manager: DialogManager) -> BStartRead: ...


class GetStartUseCaseImpl:
    def __init__(
        self,
        date_repository: DateRepository,
        telegram_auth_service: TelegramAuthServiceProtocol,
        stats_service: StatsServiceProtocol,
    ) -> None:
        self.date_repository = date_repository
        self.telegram_auth_service = telegram_auth_service
        self.stats_service = stats_service

    async def __call__(self, dialog_manager: DialogManager) -> BStartRead:
        advertiser = await self.telegram_auth_service.auth_by_dialog_manager(
            dialog_manager
        )
        if advertiser is None:
            raise ValueError()
        stats = await self.stats_service.get_stats_by_advertiser(advertiser)
        date = await self.date_repository.get_current_date()
        return StartMapper.to_read_schema(stats, advertiser, date)


class GetStartUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        date_repository: DateRepository,
        telegram_auth_service: TelegramAuthServiceProtocol,
        stats_service: StatsServiceProtocol,
    ) -> GetStartUseCaseProtocol:
        return GetStartUseCaseImpl(
            date_repository, telegram_auth_service, stats_service
        )
