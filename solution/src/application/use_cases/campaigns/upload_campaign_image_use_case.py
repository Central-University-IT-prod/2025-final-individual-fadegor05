from typing import Protocol
from uuid import UUID

from dishka import Provider, Scope, provide
from fastapi import UploadFile

from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.domain.repositories.campaign_repository import CampaignRepository
from src.infrastructure.adapters.storage_adapter import StorageAdapterProtocol
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum


class UploadCampaignImageUseCaseProtocol(Protocol):
    async def __call__(
        self, advertiser_id: UUID, campaign_id: UUID, file: UploadFile
    ) -> None: ...


class UploadCampaignImageUseCaseImpl:
    def __init__(
        self,
        advertiser_repository: AdvertiserRepository,
        campaign_repository: CampaignRepository,
        storage_adapter: StorageAdapterProtocol,
    ) -> None:
        self.advertiser_repository = advertiser_repository
        self.campaign_repository = campaign_repository
        self.storage_adapter = storage_adapter

    async def __call__(
        self, advertiser_id: UUID, campaign_id: UUID, file: UploadFile
    ) -> None:
        if file.content_type != "image/jpeg":
            raise DetailedHTTPException(ExceptionEnum.VALIDATION_ERROR)
        advertiser = await self.advertiser_repository.get_by_id_or_none(advertiser_id)
        campaign = await self.campaign_repository.get_by_id_or_none(campaign_id)
        if advertiser is None or campaign is None:
            raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
        if campaign.advertiser_id != advertiser.id:
            raise DetailedHTTPException(ExceptionEnum.NO_ACCESS)
        if campaign.image is not None:
            await self.storage_adapter.delete_file(campaign.image)
        filename = f"{campaign.id}-{file.filename}"
        await self.storage_adapter.upload_file(filename, file.file.read())
        campaign.image = filename
        await self.campaign_repository.update(campaign)


class UploadCampaignImageUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        advertiser_repository: AdvertiserRepository,
        campaign_repository: CampaignRepository,
        storage_adapter: StorageAdapterProtocol,
    ) -> UploadCampaignImageUseCaseProtocol:
        return UploadCampaignImageUseCaseImpl(
            advertiser_repository, campaign_repository, storage_adapter
        )
