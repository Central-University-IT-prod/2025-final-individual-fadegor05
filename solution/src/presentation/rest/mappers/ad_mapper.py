from src.domain.aggregates.campaign import CampaignAggregate
from src.presentation.rest.schemas.ad_schema import IAdRead


class AdMapper:
    @staticmethod
    def to_read_schema(domain: CampaignAggregate) -> IAdRead:
        return IAdRead(
            ad_id=domain.id,
            ad_title=domain.ad_title,
            ad_text=domain.ad_text,
            ad_image=f"http://localhost:8080/cdn/{domain.image}"
            if domain.image
            else None,
            advertiser_id=domain.advertiser_id,
        )
