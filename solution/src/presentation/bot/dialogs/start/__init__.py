from aiogram_dialog import Dialog

from src.presentation.bot.dialogs.start import windows


def menu_dialogs() -> list[Dialog]:
    return [
        Dialog(windows.info_window(), windows.login_window()),
        Dialog(windows.start_window()),
    ]
