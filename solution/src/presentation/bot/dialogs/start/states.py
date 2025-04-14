from aiogram.fsm.state import State, StatesGroup


class LoginMenu(StatesGroup):
    info_menu = State()
    id_menu = State()


class StartMenu(StatesGroup):
    select_menu = State()
