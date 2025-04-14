from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.use_cases.bot.get_campaign_use_case import (
    GetCampaignUseCaseProtocol,
)
from src.application.use_cases.bot.get_campaigns_use_case import (
    GetCampaignsUseCaseProtocol,
)


@inject
async def get_campaigns(
    dialog_manager: DialogManager,
    get_campaigns_use_case: FromDishka[GetCampaignsUseCaseProtocol],
    **kwargs,
) -> dict[str, str]:
    return (await get_campaigns_use_case(dialog_manager)).model_dump()


@inject
async def get_campaign(
    dialog_manager: DialogManager,
    get_campaigns_use_case: FromDishka[GetCampaignUseCaseProtocol],
    **kwargs,
) -> dict[str, str]:
    return (await get_campaigns_use_case(dialog_manager)).model_dump()
