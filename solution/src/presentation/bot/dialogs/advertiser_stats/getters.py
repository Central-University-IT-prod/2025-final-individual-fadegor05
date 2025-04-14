from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.use_cases.bot.get_stats_use_case import GetStatsUseCaseProtocol


@inject
async def get_stats(
    dialog_manager: DialogManager,
    get_stats_use_case: FromDishka[GetStatsUseCaseProtocol],
    **kwargs,
) -> dict[str, str]:
    return (await get_stats_use_case(dialog_manager)).model_dump()
