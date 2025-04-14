from src.domain.value_objects.stats import Stats, StatsDaily
from src.presentation.bot.schemas.stats_schema import BStatsDailyRead, BStatsRead


def calculate_percentage_change(prev, current):
    if prev == 0:
        return "(–%)"

    change = current - prev
    percentage_change = (change / prev) * 100

    if percentage_change >= 0:
        return f"(+{percentage_change:.1f}%)"
    else:
        return f"({percentage_change:.1f}%)"


class StatsMapper:
    @staticmethod
    def to_read_schema(domain: Stats) -> BStatsRead:
        return BStatsRead(
            impressions_count=domain.impressions_count,
            clicks_count=domain.clicks_count,
            conversion=round(domain.conversion, 1),
            spent_impressions=round(domain.spent_impressions, 1),
            spent_clicks=round(domain.spent_clicks, 1),
            spent_total=round(domain.spent_total, 1),
        )

    @staticmethod
    def to_daily_read_schema(
        domain: StatsDaily, prev_domain: StatsDaily | None
    ) -> BStatsDailyRead:
        return BStatsDailyRead(
            impressions_count=domain.impressions_count,
            clicks_count=domain.clicks_count,
            conversion=round(domain.conversion, 1),
            spent_impressions=round(domain.spent_impressions, 1),
            spent_clicks=round(domain.spent_clicks, 1),
            spent_total=round(domain.spent_total, 1),
            date=domain.date,
            impressions_count_compare=calculate_percentage_change(
                prev_domain.impressions_count, domain.impressions_count
            )
            if prev_domain is not None
            else "",
            clicks_count_compare=calculate_percentage_change(
                prev_domain.clicks_count, domain.clicks_count
            )
            if prev_domain is not None
            else "",
            conversion_compare=calculate_percentage_change(
                prev_domain.conversion, domain.conversion
            )
            if prev_domain is not None
            else "",
            spent_impressions_compare=calculate_percentage_change(
                prev_domain.spent_impressions, domain.spent_impressions
            )
            if prev_domain is not None
            else "",
            spent_clicks_compare=calculate_percentage_change(
                prev_domain.spent_clicks, domain.spent_clicks
            )
            if prev_domain is not None
            else "",
            spent_total_compare=calculate_percentage_change(
                prev_domain.spent_total, domain.spent_total
            )
            if prev_domain is not None
            else "",
        )
