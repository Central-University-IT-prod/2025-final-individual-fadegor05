from aiogram_dialog import Dialog

from src.presentation.bot.dialogs import advertiser_stats, campaign_stats, start


def dialogs() -> list[Dialog]:
    return [
        *start.menu_dialogs(),
        *campaign_stats.menu_dialogs(),
        *advertiser_stats.menu_dialogs(),
    ]
