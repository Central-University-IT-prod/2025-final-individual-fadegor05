from aiogram_dialog import Dialog

from src.presentation.bot.dialogs.campaign_stats import windows


def menu_dialogs() -> list[Dialog]:
    return [
        Dialog(windows.campaigns_window()),
        Dialog(windows.campaign_window()),
    ]
