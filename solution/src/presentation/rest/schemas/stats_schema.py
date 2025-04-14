from pydantic import BaseModel

from src.core.fields import CostField, CountField, DateField


class IStatsRead(BaseModel):
    impressions_count: CountField
    clicks_count: CountField
    conversion: float
    spent_impressions: CostField
    spent_clicks: CostField
    spent_total: CostField


class IStatsDailyRead(IStatsRead):
    date: DateField
