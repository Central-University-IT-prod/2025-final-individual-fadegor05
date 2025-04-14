from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.domain.base import BaseDomain
from src.domain.value_objects.targeting import Targeting


@dataclass
class CampaignAggregate(BaseDomain):
    cost_per_impression: Decimal
    cost_per_click: Decimal
    ad_title: str
    ad_text: str
    impressions_limit: int
    clicks_limit: int
    start_date: int
    end_date: int
    hide: bool
    image: str | None
    targeting: Targeting
    advertiser_id: UUID
