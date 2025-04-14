from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.application.use_cases.banwords.create_banwords_use_case import (
    CreateBanwordsUseCaseProtocol,
)
from src.application.use_cases.banwords.delete_banwords_use_case import (
    DeleteBanwordsUseCaseProtocol,
)
from src.application.use_cases.banwords.get_banwords_use_case import (
    GetBanwordsUseCaseProtocol,
)

router = APIRouter(
    prefix="/banwords",
    tags=["Banwords"],
    route_class=DishkaRoute,
)


@router.get("/", response_model_exclude_none=True)
async def get_banwords(
    get_banwords_use_case: FromDishka[GetBanwordsUseCaseProtocol],
) -> list[str]:
    return await get_banwords_use_case()


@router.post("/bulk", response_model_exclude_none=True)
async def add_banwords(
    objs: list[str],
    create_banwords_use_case: FromDishka[CreateBanwordsUseCaseProtocol],
) -> list[str]:
    return await create_banwords_use_case(objs)


@router.delete("/bulk", response_model_exclude_none=True)
async def delete_banwords(
    objs: list[str],
    delete_banwords_use_case: FromDishka[DeleteBanwordsUseCaseProtocol],
) -> list[str]:
    return await delete_banwords_use_case(objs)
