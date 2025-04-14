from typing import Protocol

from dishka import Provider, Scope, provide
from fastapi import Response

from src.infrastructure.adapters.storage_adapter import StorageAdapterProtocol
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum


class CDNUseCaseProtocol(Protocol):
    async def __call__(self, slug: str) -> Response: ...


class CDNUseCaseImpl:
    def __init__(
        self,
        storage_adapter: StorageAdapterProtocol,
    ) -> None:
        self.storage_adapter = storage_adapter

    async def __call__(self, slug: str) -> Response:
        data = await self.storage_adapter.get_file(slug)
        if data is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        return Response(content=data, media_type="image/jpeg")


class CDNUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        storage_adapter: StorageAdapterProtocol,
    ) -> CDNUseCaseProtocol:
        return CDNUseCaseImpl(storage_adapter)
