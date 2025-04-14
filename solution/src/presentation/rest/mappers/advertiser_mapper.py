from src.domain.entities.advertiser import AdvertiserEntity
from src.presentation.rest.schemas.advertiser_schema import IAdvertiserRead


class AdvertiserMapper:
    @staticmethod
    def to_read_schema(domain: AdvertiserEntity) -> IAdvertiserRead:
        return IAdvertiserRead(
            advertiser_id=domain.id,
            name=domain.name,
        )

    @staticmethod
    def to_domain(schema: IAdvertiserRead) -> AdvertiserEntity:
        return AdvertiserEntity(
            id=schema.advertiser_id,
            name=schema.name,
            telegram_id=None,
        )
