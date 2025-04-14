from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Next
from aiogram_dialog.widgets.text import Const, Format

from src.presentation.bot.dialogs.start import callbacks, getters, states


def info_window() -> Window:
    return Window(
        Const(
            "*Добро пожаловать в HypeAgency™* 👋\n\nЯ — ваш проводник в мир тʙᴏᴘчᴇᴄтʙᴀ и з𝖺𝗉𝖺б𝗈тka 🚀, где каждый клик имеет значение, а вся карта вашей компании будет как на ладони 🌎"
        ),
        Next(Const("Продолжить ▶️")),
        state=states.LoginMenu.info_menu,
    )


def login_window() -> Window:
    return Window(
        Const(
            "*Вы в паре нажатий от целого рекламного мира на ладони* 🤏\n\nВведите уникальный идентификатор вашей организации 💼\n\n*Например: 3fa85f64-5717-4562-b3fc-2c963f66afa6*"
        ),
        Back(Const("Назад ⬅️")),
        TextInput("advertiser_id_input", on_success=callbacks.on_advertiser_id_entered),
        state=states.LoginMenu.id_menu,
    )


def start_window() -> Window:
    return Window(
        Format(
            "*Это же HypeAgency™, а вы - {advertiser_name}* 😎\n\nНапомню, что Я — ваш проводник в мир тʙᴏᴘчᴇᴄтʙᴀ и з𝖺𝗉𝖺б𝗈тka, Вы можете посмотреть статистику за разные периоды времени, так и по определенным рекламным кампаниям 💸\n\n*Выберите пункт меню, интересующий вас* 🤔"
        ),
        Button(
            Const("Общая статистика 📈"),
            id="total_stats",
            on_click=callbacks.on_chosen_advertiser_stats,
        ),
        Button(
            Const("Статистика по рекламным кампаниям 💼"),
            id="campaings_stats",
            on_click=callbacks.on_chosen_campaigns_stats,
        ),
        Button(
            Const("Выйти из организации ◀️"),
            id="logout",
            on_click=callbacks.logout_advertiser,
        ),
        state=states.StartMenu.select_menu,
        getter=getters.get_start,
    )
