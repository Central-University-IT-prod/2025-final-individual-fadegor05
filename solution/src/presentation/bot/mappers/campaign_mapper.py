from src.domain.aggregates.campaign import CampaignAggregate
from src.domain.value_objects.stats import Stats, StatsDaily
from src.presentation.bot.mappers.stats_mapper import StatsMapper
from src.presentation.bot.schemas.campaign_schema import BCampaignBase, BCampaignRead


class CampaignMapper:
    @staticmethod
    def to_base_schema(domain: CampaignAggregate) -> BCampaignBase:
        return BCampaignBase(id=domain.id, ad_title=domain.ad_title)

    @staticmethod
    def to_read_schema(
        domain: CampaignAggregate,
        total_stats: Stats,
        daily_stats: StatsDaily,
        prev_daily_stats: StatsDaily | None,
        chosen_date: int,
        current_date: int,
    ) -> BCampaignRead:
        return BCampaignRead(
            id=domain.id,
            ad_title=domain.ad_title,
            ad_text=domain.ad_text,
            start_date=domain.start_date,
            end_date=domain.end_date,
            daily_stats=StatsMapper.to_daily_read_schema(daily_stats, prev_daily_stats),
            total_stats=StatsMapper.to_read_schema(total_stats),
            chosen_date=chosen_date,
            previous_date_str=f"◀️ {chosen_date - 1} День"
            if chosen_date != domain.start_date
            else "❌ Данных нет",
            next_date_str=f"{chosen_date + 1} День ▶️"
            if chosen_date != domain.end_date and chosen_date < current_date
            else "❌ Данных нет",
        )
