from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.application.use_cases.time.upsert_time_use_case import (
    UpsertTimeUseCaseProtocol,
)
from src.presentation.rest.schemas.time_schema import ITimeCreate, ITimeRead

router = APIRouter(prefix="/time", tags=["Time"], route_class=DishkaRoute)


@router.post("/advance")
async def post_time(
    obj: ITimeCreate, upsert_time_use_case: FromDishka[UpsertTimeUseCaseProtocol]
) -> ITimeRead:
    return await upsert_time_use_case(obj)
