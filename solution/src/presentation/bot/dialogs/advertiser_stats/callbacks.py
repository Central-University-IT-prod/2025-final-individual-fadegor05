from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.domain.repositories.date_repository import DateRepository


@inject
async def on_date_entered(
    m: Message,
    widget: TextInput,
    manager: DialogManager,
    chosen_date_str: str,
    date_repository: FromDishka[DateRepository],
    **kwargs,
):
    date = await date_repository.get_current_date()
    try:
        chosen_date = int(chosen_date_str)
    except:
        await m.answer("Неправильный формат даты ❌")
        return
    if chosen_date <= 0 or chosen_date >= date:
        await m.answer("Данных по этому дню нет ❌")
        return
    manager.start_data.update(chosen_date=chosen_date)
    await manager.show()


@inject
async def on_chosen_next(
    c: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    date_repository: FromDishka[DateRepository],
):
    if manager.start_data.get("chosen_date") < await date_repository.get_current_date():
        manager.start_data.update(chosen_date=manager.start_data.get("chosen_date") + 1)
        await manager.show()


@inject
async def on_chosen_previous(
    c: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    if manager.start_data.get("chosen_date") > 0:
        manager.start_data.update(chosen_date=manager.start_data.get("chosen_date") - 1)
        await manager.show()
