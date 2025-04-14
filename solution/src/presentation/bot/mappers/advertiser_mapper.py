from src.domain.entities.advertiser import AdvertiserEntity
from src.domain.value_objects.stats import Stats, StatsDaily
from src.presentation.bot.mappers.stats_mapper import StatsMapper
from src.presentation.bot.schemas.advertiser_schema import BAdvertiserStatsRead


class AdvertiserMapper:
    @staticmethod
    def to_read_schema(
        domain: AdvertiserEntity,
        total_stats: Stats,
        daily_stats: StatsDaily,
        prev_daily_stats: StatsDaily | None,
        chosen_date: int,
        current_date: int,
    ) -> BAdvertiserStatsRead:
        return BAdvertiserStatsRead(
            name=domain.name,
            daily_stats=StatsMapper.to_daily_read_schema(daily_stats, prev_daily_stats),
            total_stats=StatsMapper.to_read_schema(total_stats),
            chosen_date=chosen_date,
            previous_date_str=f"◀️ {chosen_date - 1} День"
            if chosen_date > 0
            else "❌ Данных нет",
            next_date_str=f"{chosen_date + 1} День ▶️"
            if chosen_date < current_date
            else "❌ Данных нет",
        )
