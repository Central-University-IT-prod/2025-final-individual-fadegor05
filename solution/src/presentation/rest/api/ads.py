from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.application.use_cases.ads.click_ad_use_case import ClickAdUseCaseProtocol
from src.application.use_cases.ads.get_ad_use_case import GetAdUseCaseProtocol
from src.presentation.rest.schemas.ad_schema import IAdClickCreate, IAdRead

router = APIRouter(prefix="/ads", tags=["Ads"], route_class=DishkaRoute)


@router.get("", response_model_exclude_none=True)
async def get_ads(
    client_id: UUID, get_ad_use_case: FromDishka[GetAdUseCaseProtocol]
) -> IAdRead:
    return await get_ad_use_case(client_id)


@router.post("/{adId}/click", status_code=204)
async def post_ads_click(
    adId: UUID,
    obj: IAdClickCreate,
    click_ad_use_case: FromDishka[ClickAdUseCaseProtocol],
):
    return await click_ad_use_case(adId, obj)
