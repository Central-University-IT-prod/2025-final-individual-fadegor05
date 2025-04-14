from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Response

from src.application.use_cases.cdn.cdn_use_case import CDNUseCaseProtocol

router = APIRouter(
    prefix="/cdn",
    tags=["CDN"],
    route_class=DishkaRoute,
)


@router.get("/{slug}")
async def cdn(slug: str, cdn_use_case: FromDishka[CDNUseCaseProtocol]) -> Response:
    return await cdn_use_case(slug)
