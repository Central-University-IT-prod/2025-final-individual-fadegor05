from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.application.use_cases.stats.get_advertiser_stats_daily_use_case import (
    GetAdvertiserStatsDailyUseCaseProtocol,
)
from src.application.use_cases.stats.get_advertiser_stats_use_case import (
    GetAdvertiserStatsUseCaseProtocol,
)
from src.application.use_cases.stats.get_campaign_stats_daily_use_case import (
    GetCampaignStatsDailyUseCaseProtocol,
)
from src.application.use_cases.stats.get_campaign_stats_use_case import (
    GetCampaignStatsUseCaseProtocol,
)
from src.presentation.rest.schemas.stats_schema import IStatsDailyRead, IStatsRead

router = APIRouter(prefix="/stats", tags=["Statistics"], route_class=DishkaRoute)


@router.get("/campaigns/{campaignId}")
async def get_campaign_stats(
    campaignId: UUID,
    get_campaign_stats_use_case: FromDishka[GetCampaignStatsUseCaseProtocol],
) -> IStatsRead:
    return await get_campaign_stats_use_case(campaignId)


@router.get("/campaigns/{campaignId}/daily")
async def get_campaign_stats_daily(
    campaignId: UUID,
    get_campaign_stats_daily_use_case: FromDishka[GetCampaignStatsDailyUseCaseProtocol],
) -> list[IStatsDailyRead]:
    return await get_campaign_stats_daily_use_case(campaignId)


@router.get("/advertisers/{advertiserId}/campaigns")
async def get_campaigns_stats_by_advertiser(
    advertiserId: UUID,
    get_advertiser_stats_use_case: FromDishka[GetAdvertiserStatsUseCaseProtocol],
) -> IStatsRead:
    return await get_advertiser_stats_use_case(advertiserId)


@router.get("/advertisers/{advertiserId}/campaigns/daily")
async def get_campaigns_stats_by_advertiser_daily(
    advertiserId: UUID,
    get_advertiser_stats_daily_use_case: FromDishka[
        GetAdvertiserStatsDailyUseCaseProtocol
    ],
) -> list[IStatsDailyRead]:
    return await get_advertiser_stats_daily_use_case(advertiserId)
