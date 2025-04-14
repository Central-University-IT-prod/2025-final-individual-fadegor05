from pydantic import BaseModel

from src.presentation.bot.schemas.stats_schema import BStatsDailyRead, BStatsRead


class BAdvertiserStatsRead(BaseModel):
    name: str
    total_stats: BStatsRead
    daily_stats: BStatsDailyRead
    chosen_date: int
    previous_date_str: str
    next_date_str: str
