from uuid import UUID

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.core.fields import AdTextField, CostField, DateField, LimitField
from src.presentation.rest.schemas.targeting_schema import ITargetRead


class ICampaignCreate(BaseModel):
    cost_per_impression: CostField
    cost_per_click: CostField
    ad_title: AdTextField
    ad_text: AdTextField
    targeting: ITargetRead | None = None
    impressions_limit: LimitField
    clicks_limit: LimitField
    start_date: DateField
    end_date: DateField

    @field_validator("end_date")
    def validate_age_until(cls, value: int | None, info: FieldValidationInfo):
        start_date = info.data.get("start_date")
        if start_date is not None and value is not None and value < start_date:
            raise ValueError("end_date должно быть больше или равно start_date")
        return value

    @field_validator("clicks_limit")
    def validate_clicks_limit(cls, value: int | None, info: FieldValidationInfo):
        impressions_limit = info.data.get("impressions_limit", 0)
        if value > impressions_limit:
            raise ValueError(
                "impressions_limit должно быть больше или равно clicks_limit"
            )
        return value


class ICampaignRead(ICampaignCreate):
    image: str | None = None
    campaign_id: UUID
    advertiser_id: UUID
