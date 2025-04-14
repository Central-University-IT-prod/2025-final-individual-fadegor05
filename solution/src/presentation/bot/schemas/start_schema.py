from pydantic import BaseModel


class BStartRead(BaseModel):
    date: int
    advertiser_name: str
    impressions_count: int
    clicks_count: int
    conversion: float
    spent_impressions: float
    spent_clicks: float
    spent_total: float
