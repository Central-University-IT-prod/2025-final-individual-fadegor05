from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, File, Query, UploadFile

from src.application.use_cases.campaigns.create_campaign_use_case import (
    CreateCampaignUseCaseProtocol,
)
from src.application.use_cases.campaigns.delete_campaign_image_use_case import (
    DeleteCampaignImageUseCaseProtocol,
)
from src.application.use_cases.campaigns.delete_campaign_use_case import (
    DeleteCampaignUseCaseProtocol,
)
from src.application.use_cases.campaigns.get_campaign_use_case import (
    GetCampaignUseCaseProtocol,
)
from src.application.use_cases.campaigns.get_campaigns_use_case import (
    GetCampaignsUseCaseProtocol,
)
from src.application.use_cases.campaigns.update_campaign_use_case import (
    UpdateCampaignUseCaseProtocol,
)
from src.application.use_cases.campaigns.upload_campaign_image_use_case import (
    UploadCampaignImageUseCaseProtocol,
)
from src.presentation.rest.schemas.campaign_schema import (
    ICampaignCreate,
    ICampaignRead,
)
from src.presentation.rest.schemas.common_schema import IPaginationCommon

router = APIRouter(
    prefix="/advertisers/{advertiserId}/campaigns",
    tags=["Campaigns"],
    route_class=DishkaRoute,
)


@router.post("", status_code=201, response_model_exclude_none=True)
async def create_campaigns(
    advertiserId: UUID,
    obj: ICampaignCreate,
    create_campaign_use_case: FromDishka[CreateCampaignUseCaseProtocol],
) -> ICampaignRead:
    return await create_campaign_use_case(advertiserId, obj)


@router.get("", response_model_exclude_none=True)
async def get_campaigns(
    advertiserId: UUID,
    pagination: Annotated[IPaginationCommon, Query()],
    get_campaigns_use_case: FromDishka[GetCampaignsUseCaseProtocol],
) -> list[ICampaignRead]:
    return await get_campaigns_use_case(advertiserId, pagination)


@router.get("/{campaignId}", response_model_exclude_none=True)
async def get_campaign(
    advertiserId: UUID,
    campaignId: UUID,
    get_campaign_use_case: FromDishka[GetCampaignUseCaseProtocol],
) -> ICampaignRead:
    return await get_campaign_use_case(advertiserId, campaignId)


@router.put("/{campaignId}", response_model_exclude_none=True)
async def put_campaign(
    advertiserId: UUID,
    campaignId: UUID,
    obj: ICampaignCreate,
    update_campaign_use_case: FromDishka[UpdateCampaignUseCaseProtocol],
) -> ICampaignRead:
    return await update_campaign_use_case(advertiserId, campaignId, obj)


@router.delete("/{campaignId}", status_code=204)
async def delete_campaign(
    advertiserId: UUID,
    campaignId: UUID,
    delete_campaign_use_case: FromDishka[DeleteCampaignUseCaseProtocol],
):
    await delete_campaign_use_case(advertiserId, campaignId)


@router.post("/{campaignId}/image", status_code=200, response_model_exclude_none=True)
async def upload_campaign_image(
    advertiserId: UUID,
    campaignId: UUID,
    upload_campaign_image_use_case: FromDishka[UploadCampaignImageUseCaseProtocol],
    obj: UploadFile = File(...),
):
    await upload_campaign_image_use_case(advertiserId, campaignId, obj)


@router.delete("/{campaignId}/image", status_code=200, response_model_exclude_none=True)
async def delete_campaign_image(
    advertiserId: UUID,
    campaignId: UUID,
    delete_campaign_image_use_case: FromDishka[DeleteCampaignImageUseCaseProtocol],
):
    await delete_campaign_image_use_case(advertiserId, campaignId)
