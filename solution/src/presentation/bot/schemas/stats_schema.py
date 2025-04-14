from decimal import Decimal

from pydantic import BaseModel


class BStatsRead(BaseModel):
    impressions_count: int
    clicks_count: int
    conversion: float
    spent_impressions: Decimal
    spent_clicks: Decimal
    spent_total: Decimal


class BStatsDailyRead(BStatsRead):
    date: int
    impressions_count_compare: str
    clicks_count_compare: str
    conversion_compare: str
    spent_impressions_compare: str
    spent_clicks_compare: str
    spent_total_compare: str
