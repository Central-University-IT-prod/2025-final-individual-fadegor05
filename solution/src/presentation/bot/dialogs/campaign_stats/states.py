from aiogram.fsm.state import State, StatesGroup


class CampaignsMenu(StatesGroup):
    select_menu = State()


class CampaignMenu(StatesGroup):
    info_menu = State()
