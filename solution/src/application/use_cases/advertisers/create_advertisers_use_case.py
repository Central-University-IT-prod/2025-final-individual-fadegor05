from dishka import Provider, Scope, provide

from src.core.use_case import UseCaseProtocol
from src.domain.entities.advertiser import AdvertiserEntity
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.advertiser_mapper import AdvertiserMapper
from src.presentation.rest.schemas.advertiser_schema import IAdvertiserRead

CreateAdvertisersUseCaseProtocol = UseCaseProtocol[list[IAdvertiserRead]]


class CreateAdvertisersUseCaseImpl:
    def __init__(self, advertiser_repository: AdvertiserRepository) -> None:
        self.advertiser_repository = advertiser_repository

    async def __call__(self, objs: list[IAdvertiserRead]) -> list[IAdvertiserRead]:
        advertisers: list[AdvertiserEntity] = [
            AdvertiserMapper.to_domain(obj) for obj in objs
        ]
        added_advertisers = await self.advertiser_repository.bulk_update(advertisers)
        if added_advertisers is None:
            raise DetailedHTTPException(ExceptionEnum.ALREADY_EXISTS)
        return [
            AdvertiserMapper.to_read_schema(advertiser)
            for advertiser in added_advertisers
        ]


class CreateAdvertisersUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self, advertiser_repository: AdvertiserRepository
    ) -> CreateAdvertisersUseCaseProtocol:
        return CreateAdvertisersUseCaseImpl(advertiser_repository)
