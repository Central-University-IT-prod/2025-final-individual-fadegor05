from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide

from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.domain.repositories.campaign_repository import CampaignRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.mappers.campaign_mapper import CampaignMapper
from src.presentation.rest.mappers.pagination_mapper import PaginationMapper
from src.presentation.rest.schemas.campaign_schema import ICampaignRead
from src.presentation.rest.schemas.common_schema import IPaginationCommon


class GetCampaignsUseCaseProtocol(Protocol):
    async def __call__(
        self, advertiser_id: UUID, pagination: IPaginationCommon
    ) -> list[ICampaignRead]: ...


class GetCampaignsUseCaseImpl:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        advertiser_repository: AdvertiserRepository,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.advertiser_repository = advertiser_repository

    async def __call__(
        self, advertiser_id: UUID, pagination: IPaginationCommon
    ) -> list[ICampaignRead]:
        advertiser = await self.advertiser_repository.get_by_id_or_none(advertiser_id)
        if advertiser is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        campaigns = await self.campaign_repository.get_paginated_by_advertiser_id(
            PaginationMapper.to_domain(pagination), advertiser_id
        )
        return [CampaignMapper.to_read_schema(campaign) for campaign in campaigns]


class GetCampaignsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repository: CampaignRepository,
        advertiser_repository: AdvertiserRepository,
    ) -> GetCampaignsUseCaseProtocol:
        return GetCampaignsUseCaseImpl(campaign_repository, advertiser_repository)
