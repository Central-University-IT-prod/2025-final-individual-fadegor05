from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.application.use_cases.advertisers.create_advertisers_use_case import (
    CreateAdvertisersUseCaseProtocol,
)
from src.application.use_cases.advertisers.get_advertiser_use_case import (
    GetAdvertiserUseCaseProtocol,
)
from src.application.use_cases.advertisers.upsert_ml_scores_use_case import (
    UpsertMLScoresUseCaseProtocol,
)
from src.presentation.rest.schemas.advertiser_schema import IAdvertiserRead
from src.presentation.rest.schemas.ml_score_schema import IMLScoreRead

router = APIRouter(prefix="", tags=["Advertisers"], route_class=DishkaRoute)


@router.get("/advertisers/{advertiserId}")
async def get_advertiser(
    advertiserId: UUID,
    get_advertiser_use_case: FromDishka[GetAdvertiserUseCaseProtocol],
) -> IAdvertiserRead:
    return await get_advertiser_use_case(advertiserId)


@router.post("/advertisers/bulk", status_code=201)
async def create_advertisers(
    objs: list[IAdvertiserRead],
    create_advertisers_use_case: FromDishka[CreateAdvertisersUseCaseProtocol],
) -> list[IAdvertiserRead]:
    return await create_advertisers_use_case(objs)


@router.post("/ml-scores")
async def post_ml_scores(
    obj: IMLScoreRead,
    upsert_ml_scores_use_case: FromDishka[UpsertMLScoresUseCaseProtocol],
) -> None:
    return await upsert_ml_scores_use_case(obj)
