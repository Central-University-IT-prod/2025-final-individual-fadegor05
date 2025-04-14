from typing import Protocol
from uuid import UUID, uuid4

from dishka import Provider, Scope, provide

from src.application.services.ad_service import AdServiceProtocol
from src.domain.aggregates.impression import ImpressionAggregate
from src.domain.repositories.campaign_repository import CampaignRepository
from src.domain.repositories.client_repository import ClientRepository
from src.domain.repositories.date_repository import DateRepository
from src.domain.repositories.impression_repository import ImpressionRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.ad_mapper import AdMapper
from src.presentation.rest.schemas.ad_schema import IAdRead


class GetAdUseCaseProtocol(Protocol):
    async def __call__(self, client_id: UUID) -> IAdRead: ...


class GetAdUseCaseImpl:
    def __init__(
        self,
        client_repository: ClientRepository,
        campaign_repository: CampaignRepository,
        impression_repository: ImpressionRepository,
        date_repository: DateRepository,
        ad_service: AdServiceProtocol,
    ) -> None:
        self.client_repository = client_repository
        self.campaign_repository = campaign_repository
        self.impression_repository = impression_repository
        self.date_repository = date_repository
        self.ad_service = ad_service

    async def __call__(self, client_id: UUID) -> IAdRead:
        client = await self.client_repository.get_by_id_or_none(client_id)
        if client is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        ad = await self.ad_service.get_ad(client)
        if ad is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        impression = (
            await self.impression_repository.get_by_campaign_id_and_client_id_or_none(
                ad.id, client.id
            )
        )
        if impression is None:
            current_date = await self.date_repository.get_current_date()
            await self.impression_repository.create(
                ImpressionAggregate(
                    uuid4(), client.id, ad.id, ad.cost_per_impression, current_date
                )
            )
        return AdMapper.to_read_schema(ad)


class GetAdUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        client_repository: ClientRepository,
        campaign_repository: CampaignRepository,
        impression_repository: ImpressionRepository,
        date_repository: DateRepository,
        ad_service: AdServiceProtocol,
    ) -> GetAdUseCaseProtocol:
        return GetAdUseCaseImpl(
            client_repository,
            campaign_repository,
            impression_repository,
            date_repository,
            ad_service,
        )
