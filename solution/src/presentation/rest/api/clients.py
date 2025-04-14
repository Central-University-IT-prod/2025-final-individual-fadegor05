from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.application.use_cases.clients.create_clients_use_case import (
    CreateClientsUseCaseProtocol,
)
from src.application.use_cases.clients.get_client_use_case import (
    GetClientUseCaseProtocol,
)
from src.presentation.rest.schemas.client_schema import IClientRead

router = APIRouter(prefix="/clients", tags=["Clients"], route_class=DishkaRoute)


@router.get("/{clientId}")
async def get_client(
    clientId: UUID,
    get_client_use_case: FromDishka[GetClientUseCaseProtocol],
) -> IClientRead:
    return await get_client_use_case(clientId)


@router.post("/bulk", status_code=201)
async def create_clients(
    objs: list[IClientRead],
    create_clients_use_case: FromDishka[CreateClientsUseCaseProtocol],
) -> list[IClientRead]:
    return await create_clients_use_case(objs)
