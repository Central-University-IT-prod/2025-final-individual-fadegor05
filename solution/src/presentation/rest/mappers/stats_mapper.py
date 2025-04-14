from src.domain.value_objects.stats import Stats, StatsDaily
from src.presentation.rest.schemas.stats_schema import IStatsDailyRead, IStatsRead


class StatsMapper:
    @staticmethod
    def to_read_schema(domain: Stats) -> IStatsRead:
        return IStatsRead(
            impressions_count=domain.impressions_count,
            clicks_count=domain.clicks_count,
            conversion=domain.conversion,
            spent_impressions=float(domain.spent_impressions),
            spent_clicks=float(domain.spent_clicks),
            spent_total=float(domain.spent_total),
        )

    @staticmethod
    def to_read_schema_daily(domain: StatsDaily) -> IStatsDailyRead:
        return IStatsDailyRead(
            impressions_count=domain.impressions_count,
            clicks_count=domain.clicks_count,
            conversion=domain.conversion,
            spent_impressions=float(domain.spent_impressions),
            spent_clicks=float(domain.spent_clicks),
            spent_total=float(domain.spent_total),
            date=domain.date,
        )
