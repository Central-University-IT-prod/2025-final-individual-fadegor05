from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Stats:
    impressions_count: int
    clicks_count: int
    conversion: float
    spent_impressions: Decimal
    spent_clicks: Decimal
    spent_total: Decimal


@dataclass
class StatsDaily(Stats):
    date: int
