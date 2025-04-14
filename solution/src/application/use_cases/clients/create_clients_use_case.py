from typing import Protocol

from dishka import Provider, Scope, provide

from src.domain.entities.client import ClientEntity
from src.domain.repositories.client_repository import ClientRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.client_mapper import ClientMapper
from src.presentation.rest.schemas.client_schema import IClientRead


class CreateClientsUseCaseProtocol(Protocol):
    async def __call__(self, objs: list[IClientRead]) -> list[IClientRead]: ...


class CreateClientsUseCaseImpl:
    def __init__(self, client_repository: ClientRepository) -> None:
        self.client_repository = client_repository

    async def __call__(self, objs: list[IClientRead]) -> list[IClientRead]:
        clients: list[ClientEntity] = [ClientMapper.to_domain(obj) for obj in objs]
        added_clients = await self.client_repository.bulk_update(clients)
        if added_clients is None:
            raise DetailedHTTPException(ExceptionEnum.ALREADY_EXISTS)
        return [ClientMapper.to_read_schema(client) for client in added_clients]


class CreateClientsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self, client_repository: ClientRepository
    ) -> CreateClientsUseCaseProtocol:
        return CreateClientsUseCaseImpl(client_repository)
