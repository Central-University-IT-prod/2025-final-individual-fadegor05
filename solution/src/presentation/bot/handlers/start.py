from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import FromDishka, inject

from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.presentation.bot.dialogs.start.states import LoginMenu, StartMenu
from src.presentation.bot.handlers.router import router


@router.message(CommandStart())
@inject
async def start_handler(
    message: Message,
    dialog_manager: DialogManager,
    advertiser_repository: FromDishka[AdvertiserRepository],
) -> None:
    telegram_id = int(message.from_user.id)  # type: ignore
    advertiser = await advertiser_repository.get_by_telegram_id_or_none(telegram_id)
    if advertiser is None:
        await dialog_manager.start(LoginMenu.info_menu, mode=StartMode.RESET_STACK)
        return
    await dialog_manager.start(
        StartMenu.select_menu,
        mode=StartMode.RESET_STACK,
        data={"advertiser_id": advertiser.id},
    )
