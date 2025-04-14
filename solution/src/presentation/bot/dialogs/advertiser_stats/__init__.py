from aiogram_dialog import Dialog

from src.presentation.bot.dialogs.advertiser_stats import windows


def menu_dialogs() -> list[Dialog]:
    return [
        Dialog(windows.stats_window()),
    ]
