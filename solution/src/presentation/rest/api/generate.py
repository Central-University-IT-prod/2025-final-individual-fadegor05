from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.application.use_cases.generate.generate_text_use_case import (
    GenerateTextUseCaseProtocol,
)
from src.presentation.rest.schemas.generate_schema import (
    IGenerateTextCreate,
    IGenerateTextRead,
)

router = APIRouter(
    prefix="/advertisers/{advertiserId}/generate",
    tags=["Generate"],
    route_class=DishkaRoute,
)


@router.post("/text")
async def generate_text(
    advertiserId: UUID,
    obj: IGenerateTextCreate,
    generate_text_use_case: FromDishka[GenerateTextUseCaseProtocol],
) -> IGenerateTextRead:
    return await generate_text_use_case(advertiserId, obj)
