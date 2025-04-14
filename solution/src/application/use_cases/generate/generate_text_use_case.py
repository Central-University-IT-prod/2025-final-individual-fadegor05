from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.application.services.content_generation_serivce import (
    ContentGenerationServiceProtocol,
)
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.schemas.generate_schema import (
    IGenerateTextCreate,
    IGenerateTextRead,
)


class GenerateTextUseCaseProtocol(Protocol):
    async def __call__(
        self, advertiser_id: UUID, obj: IGenerateTextCreate
    ) -> IGenerateTextRead: ...


class GenerateTextUseCaseImpl:
    def __init__(
        self,
        advertiser_repository: AdvertiserRepository,
        content_generation_service: ContentGenerationServiceProtocol,
    ) -> None:
        self.advertiser_repository = advertiser_repository
        self.content_generation_service = content_generation_service

    async def __call__(
        self, advertiser_id: UUID, obj: IGenerateTextCreate
    ) -> IGenerateTextRead:
        advertiser = await self.advertiser_repository.get_by_id_or_none(advertiser_id)
        if advertiser is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        text = await self.content_generation_service.generate_text(
            obj.title, advertiser.name
        )
        return IGenerateTextRead(title=obj.title, text=text)


class GenerateTextUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        advertiser_repository: AdvertiserRepository,
        content_generation_service: ContentGenerationServiceProtocol,
    ) -> GenerateTextUseCaseProtocol:
        return GenerateTextUseCaseImpl(
            advertiser_repository, content_generation_service
        )
