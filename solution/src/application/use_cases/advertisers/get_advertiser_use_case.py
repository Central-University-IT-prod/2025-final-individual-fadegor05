from uuid import UUID

from dishka import Provider, Scope, provide

from src.core.use_case import UseCaseProtocol
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.advertiser_mapper import AdvertiserMapper
from src.presentation.rest.schemas.advertiser_schema import IAdvertiserRead

GetAdvertiserUseCaseProtocol = UseCaseProtocol[IAdvertiserRead]


class GetAdvertiserUseCaseImpl:
    def __init__(self, advertiser_repository: AdvertiserRepository) -> None:
        self.advertiser_repository = advertiser_repository

    async def __call__(self, client_id: UUID) -> IAdvertiserRead:
        client = await self.advertiser_repository.get_by_id_or_none(client_id)
        if client is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        return AdvertiserMapper.to_read_schema(client)


class GetAdvertiserUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self, advertiser_repository: AdvertiserRepository
    ) -> GetAdvertiserUseCaseProtocol:
        return GetAdvertiserUseCaseImpl(advertiser_repository)
