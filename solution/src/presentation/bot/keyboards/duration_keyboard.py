import operator

from aiogram_dialog.widgets.kbd import Radio
from aiogram_dialog.widgets.text import Format

duration_keyboard = Radio(
    Format("🔘 {item[0]}"),
    Format("⚪️ {item[0]}"),
    id="r_durations",
    item_id_getter=operator.itemgetter(1),
    items="durations",
)
