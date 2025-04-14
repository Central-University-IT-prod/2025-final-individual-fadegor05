from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format

from src.presentation.bot.dialogs.advertiser_stats import callbacks, getters, states


def stats_window() -> Window:
    return Window(
        Format(
            """
*Ваша статистика {name}* 📊
*• Общая* 🧳
▸ Показов: {total_stats[impressions_count]}
▸ Переходов: {total_stats[clicks_count]}
▸ Конверсия: {total_stats[conversion]}%
▸ Затраты на показы: {total_stats[spent_impressions]}₽
▸ Затраты на переходы: {total_stats[spent_clicks]}₽
▸ Затраты всего: {total_stats[spent_total]}₽

*• {daily_stats[date]} День* 💸
▸ Показов: {daily_stats[impressions_count]} {daily_stats[impressions_count_compare]}
▸ Переходов: {daily_stats[clicks_count]} {daily_stats[clicks_count_compare]}
▸ Конверсия: {daily_stats[conversion]}% {daily_stats[conversion_compare]}
▸ Затраты на показы: {daily_stats[spent_impressions]}₽ {daily_stats[spent_impressions_compare]}
▸ Затраты на переходы: {daily_stats[spent_clicks]}₽ {daily_stats[spent_clicks_compare]}
▸ Затраты всего: {daily_stats[spent_total]}₽ {daily_stats[spent_total_compare]}

*Напишите или выберите день, статистика которого интересует вас* 🤔
"""
        ),
        Row(
            Button(
                Format("{previous_date_str}"),
                id="previous_date",
                on_click=callbacks.on_chosen_previous,
            ),
            Button(Format("{daily_stats[date]} День ❇️"), id="current_date"),
            Button(
                Format("{next_date_str}"),
                id="next_date",
                on_click=callbacks.on_chosen_next,
            ),
        ),
        Cancel(Const("Назад ⬅️")),
        TextInput("advertiser_id_input", on_success=callbacks.on_date_entered),
        state=states.StatsMenu.info_menu,
        getter=getters.get_stats,
    )
