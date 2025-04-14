from typing import Protocol, Self

from aiogram_dialog import DialogManager
from dishka import Provider, Scope, provide

from src.domain.entities.advertiser import AdvertiserEntity
from src.domain.repositories.advertiser_repository import AdvertiserRepository


class TelegramAuthServiceProtocol(Protocol):
    async def auth_by_telegram_id(self: Self, telegram_id: int) -> AdvertiserEntity: ...

    async def auth_by_dialog_manager(
        self: Self, dialog_manager: DialogManager
    ) -> AdvertiserEntity: ...


class TelegramAuthServiceImpl:
    def __init__(self, advertiser_repository: AdvertiserRepository) -> None:
        self.advertiser_repository = advertiser_repository

    async def auth_by_telegram_id(self: Self, telegram_id: int) -> AdvertiserEntity:
        advertiser = await self.advertiser_repository.get_by_telegram_id_or_none(
            telegram_id
        )
        if advertiser is None:
            raise ValueError()
        return advertiser

    async def auth_by_dialog_manager(
        self, dialog_manager: DialogManager
    ) -> AdvertiserEntity:
        telegram_id = dialog_manager.middleware_data.get("event_chat").id  # type: ignore
        return await self.auth_by_telegram_id(telegram_id)


class TelegramAuthServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self, advertiser_repository: AdvertiserRepository
    ) -> TelegramAuthServiceProtocol:
        return TelegramAuthServiceImpl(advertiser_repository)
