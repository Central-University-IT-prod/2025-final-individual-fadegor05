from typing import Protocol
from uuid import UUID, uuid4

from dishka import Provider, Scope, provide

from src.domain.aggregates.click import ClickAggregate
from src.domain.repositories.campaign_repository import CampaignRepository
from src.domain.repositories.click_repository import ClickRepository
from src.domain.repositories.client_repository import ClientRepository
from src.domain.repositories.date_repository import DateRepository
from src.domain.repositories.impression_repository import ImpressionRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.schemas.ad_schema import IAdClickCreate


class ClickAdUseCaseProtocol(Protocol):
    async def __call__(self, ad_id: UUID, obj: IAdClickCreate) -> None: ...


class ClickAdUseCaseImpl:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        impression_repository: ImpressionRepository,
        click_repository: ClickRepository,
        client_repository: ClientRepository,
        date_repository: DateRepository,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.impression_repository = impression_repository
        self.click_repository = click_repository
        self.client_repository = client_repository
        self.date_repository = date_repository

    async def __call__(self, ad_id: UUID, obj: IAdClickCreate) -> None:
        click = await self.click_repository.get_by_campaign_id_and_client_id_or_none(
            ad_id, obj.client_id
        )
        if click is not None:
            return
        campaign = await self.campaign_repository.get_by_id_or_none(ad_id)
        if campaign is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        client = await self.client_repository.get_by_id_or_none(obj.client_id)
        if client is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        click = await self.click_repository.get_by_campaign_id_and_client_id_or_none(
            campaign.id, obj.client_id
        )
        if click is not None:
            return
        clicks_amount = await self.click_repository.get_amount_by_campaign_id(
            campaign.id
        )
        if clicks_amount >= campaign.clicks_limit:
            raise DetailedHTTPException(ExceptionEnum.VALIDATION_ERROR)
        impression = (
            await self.impression_repository.get_by_campaign_id_and_client_id_or_none(
                campaign.id, obj.client_id
            )
        )
        if impression is None:
            raise DetailedHTTPException(ExceptionEnum.NO_ACCESS)
        date = await self.date_repository.get_current_date()
        await self.click_repository.create(
            ClickAggregate(
                id=uuid4(),
                client_id=obj.client_id,
                campaign_id=campaign.id,
                cost=campaign.cost_per_click,
                date=date,
            )
        )


class ClickAdUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repository: CampaignRepository,
        impression_repository: ImpressionRepository,
        click_repository: ClickRepository,
        client_repository: ClientRepository,
        date_repository: DateRepository,
    ) -> ClickAdUseCaseProtocol:
        return ClickAdUseCaseImpl(
            campaign_repository,
            impression_repository,
            click_repository,
            client_repository,
            date_repository,
        )
