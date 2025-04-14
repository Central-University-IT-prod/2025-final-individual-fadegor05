from decimal import Decimal
from uuid import UUID, uuid4

from src.domain.aggregates.campaign import CampaignAggregate
from src.domain.value_objects.targeting import Targeting
from src.presentation.rest.mappers.targeting_mapper import TargetingMapper
from src.presentation.rest.schemas.campaign_schema import (
    ICampaignCreate,
    ICampaignRead,
)


class CampaignMapper:
    @staticmethod
    def to_read_schema(domain: CampaignAggregate) -> ICampaignRead:
        return ICampaignRead(
            cost_per_impression=float(domain.cost_per_impression),
            cost_per_click=float(domain.cost_per_click),
            ad_title=domain.ad_title,
            ad_text=domain.ad_text,
            targeting=TargetingMapper.to_read_schema(domain.targeting),
            impressions_limit=domain.impressions_limit,
            clicks_limit=domain.clicks_limit,
            start_date=domain.start_date,
            end_date=domain.end_date,
            image=f"http://localhost:8080/cdn/{domain.image}"
            if domain.image is not None
            else None,
            campaign_id=domain.id,
            advertiser_id=domain.advertiser_id,
        )

    @staticmethod
    def to_domain(schema: ICampaignCreate, advertiser_id: UUID) -> CampaignAggregate:
        return CampaignAggregate(
            id=uuid4(),
            cost_per_impression=Decimal(schema.cost_per_impression),
            cost_per_click=Decimal(schema.cost_per_click),
            ad_title=schema.ad_title,
            ad_text=schema.ad_text,
            targeting=TargetingMapper.to_domain(schema.targeting)
            if schema.targeting
            else Targeting(gender=None, age_from=None, age_to=None, location=None),
            impressions_limit=schema.impressions_limit,
            clicks_limit=schema.clicks_limit,
            start_date=schema.start_date,
            end_date=schema.end_date,
            hide=False,
            image=None,
            advertiser_id=advertiser_id,
        )

    @staticmethod
    def update_domain(
        domain: CampaignAggregate, schema: ICampaignCreate, current_date: int
    ) -> CampaignAggregate | None:
        if schema.start_date <= current_date and (
            domain.impressions_limit != schema.impressions_limit
            or domain.clicks_limit != schema.clicks_limit
            or domain.start_date != schema.start_date
            or domain.end_date != schema.end_date
        ):
            return None
        domain.impressions_limit = schema.impressions_limit
        domain.clicks_limit = schema.clicks_limit
        domain.cost_per_impression = Decimal(schema.cost_per_impression)
        domain.cost_per_click = Decimal(schema.cost_per_click)
        domain.ad_title = schema.ad_title
        domain.ad_text = schema.ad_text
        domain.start_date = schema.start_date
        domain.end_date = schema.end_date
        if schema.targeting is not None:
            domain.targeting = TargetingMapper.to_domain(schema.targeting)
        return domain
