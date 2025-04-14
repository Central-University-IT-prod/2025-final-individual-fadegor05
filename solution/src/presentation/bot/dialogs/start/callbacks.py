from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.services.telegram_auth_service import TelegramAuthServiceProtocol
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.domain.repositories.date_repository import DateRepository
from src.presentation.bot.dialogs.advertiser_stats.states import StatsMenu
from src.presentation.bot.dialogs.campaign_stats.states import CampaignsMenu
from src.presentation.bot.dialogs.start.states import LoginMenu, StartMenu


@inject
async def on_advertiser_id_entered(
    m: Message,
    widget: TextInput,
    manager: DialogManager,
    advertiser_id_str: str,
    advertiser_repository: FromDishka[AdvertiserRepository],
    **kwargs,
):
    try:
        advertiser_id = UUID(advertiser_id_str)
        advertiser = await advertiser_repository.get_by_id_or_none(advertiser_id)
    except:
        await m.answer("Неверный уникальный идентификатор ❌")
        return
    if advertiser is None:
        await m.answer("Неверный уникальный идентификатор ❌")
        return
    if advertiser.telegram_id is not None:
        await m.answer("Данная организация уже привязана ❌")
        return
    telegram_id = manager.middleware_data.get("event_chat").id  # type: ignore
    advertiser.telegram_id = telegram_id
    await advertiser_repository.update(advertiser)
    await manager.start(
        StartMenu.select_menu,
        mode=StartMode.RESET_STACK,
        data={"advertiser_id": advertiser_id},
    )


@inject
async def logout_advertiser(
    c: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    telegram_auth_service: FromDishka[TelegramAuthServiceProtocol],
    advertiser_repository: FromDishka[AdvertiserRepository],
):
    try:
        advertiser = await telegram_auth_service.auth_by_dialog_manager(manager)
        advertiser.telegram_id = None
        await advertiser_repository.update(advertiser)
    finally:
        c.answer("Вы успешно вышли из организации 🚪")
        await manager.start(
            LoginMenu.info_menu,
            mode=StartMode.RESET_STACK,
        )


@inject
async def on_chosen_campaigns_stats(
    c: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    await manager.start(CampaignsMenu.select_menu)


@inject
async def on_chosen_advertiser_stats(
    c: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    date_repostiory: FromDishka[DateRepository],
):
    await manager.start(
        StatsMenu.info_menu,
        data={"chosen_date": await date_repostiory.get_current_date()},
    )
