import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_campaigns(on_click):
    return ScrollingGroup(
        Select(
            Format("💼 {item[ad_title]}"),
            id="s_scroll_campaigns",
            item_id_getter=operator.itemgetter("id"),
            items="campaigns",
            on_click=on_click,
        ),
        id="campaings_id",
        width=1,
        height=5,
    )
