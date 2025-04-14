from uuid import UUID

from pydantic import BaseModel

from src.presentation.bot.schemas.stats_schema import BStatsDailyRead, BStatsRead


class BCampaignBase(BaseModel):
    id: UUID
    ad_title: str


class BCampaignRead(BCampaignBase):
    ad_text: str
    start_date: int
    end_date: int
    daily_stats: BStatsDailyRead
    total_stats: BStatsRead
    chosen_date: int
    previous_date_str: str
    next_date_str: str


class BCampaignsRead(BaseModel):
    campaigns: list[BCampaignBase]
