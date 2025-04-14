from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.use_cases.bot.get_start_use_case import GetStartUseCaseProtocol


@inject
async def get_start(
    dialog_manager: DialogManager,
    get_start_use_case: FromDishka[GetStartUseCaseProtocol],
    **kwargs,
) -> dict[str, str]:
    return (await get_start_use_case(dialog_manager)).model_dump()
