from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.domain.repositories.client_repository import ClientRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.client_mapper import ClientMapper
from src.presentation.rest.schemas.client_schema import IClientRead


class GetClientUseCaseProtocol(Protocol):
    async def __call__(self, id: UUID) -> IClientRead: ...


class GetClientUseCaseImpl:
    def __init__(self, client_repository: ClientRepository) -> None:
        self.client_repository = client_repository

    async def __call__(self, id: UUID) -> IClientRead:
        client = await self.client_repository.get_by_id_or_none(id)
        if client is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        return ClientMapper.to_read_schema(client)


class GetClientUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self, client_repository: ClientRepository
    ) -> GetClientUseCaseProtocol:
        return GetClientUseCaseImpl(client_repository)
