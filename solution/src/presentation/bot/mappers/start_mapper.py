from src.domain.entities.advertiser import AdvertiserEntity
from src.domain.value_objects.stats import Stats
from src.presentation.bot.schemas.start_schema import BStartRead


class StartMapper:
    @staticmethod
    def to_read_schema(
        stats: Stats, advertiser: AdvertiserEntity, date: int
    ) -> BStartRead:
        return BStartRead(
            date=date,
            advertiser_name=advertiser.name,
            impressions_count=stats.impressions_count,
            clicks_count=stats.clicks_count,
            conversion=round(stats.conversion, 2),
            spent_impressions=float(stats.spent_impressions),
            spent_clicks=float(stats.spent_clicks),
            spent_total=float(stats.spent_total),
        )
