from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.domain.repositories.campaign_repository import CampaignRepository
from src.domain.repositories.date_repository import DateRepository
from src.presentation.bot.dialogs.campaign_stats.states import (
    CampaignMenu,
)


@inject
async def on_chosen_campaign(
    c: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    campaign_id: str,
    campaign_repository: FromDishka[CampaignRepository],
    date_repository: FromDishka[DateRepository],
    **kwargs,
):
    date = await date_repository.get_current_date()
    campaign = await campaign_repository.get_by_id_or_none(campaign_id)
    if campaign is None:
        raise ValueError()
    if date < campaign.start_date:
        await c.answer(
            "По данной рекламной кампании отсутствует статистика, так как она еще не началась ❌"
        )
        return
    chosen_date = campaign.start_date
    if date <= campaign.end_date:
        chosen_date = date
    await manager.start(
        CampaignMenu.info_menu,
        {
            "campaign_id": campaign_id,
            "chosen_date": chosen_date,
            "start_date": campaign.start_date,
            "end_date": campaign.end_date,
        },
    )


@inject
async def on_chosen_next(
    c: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    date_repository: FromDishka[DateRepository],
):
    if (
        manager.start_data.get("chosen_date") < manager.start_data.get("end_date")
        and manager.start_data.get("chosen_date")
        < await date_repository.get_current_date()
    ):
        manager.start_data.update(chosen_date=manager.start_data.get("chosen_date") + 1)
        await manager.show()


@inject
async def on_chosen_previous(
    c: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    if manager.start_data.get("chosen_date") > manager.start_data.get("start_date"):
        manager.start_data.update(chosen_date=manager.start_data.get("chosen_date") - 1)
        await manager.show()
