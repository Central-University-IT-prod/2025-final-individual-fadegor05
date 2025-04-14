from typing import Protocol, Self

from dishka import Provider, Scope, provide

from src.domain.aggregates.campaign import CampaignAggregate
from src.domain.entities.client import ClientEntity
from src.domain.repositories.campaign_repository import CampaignRepository
from src.domain.repositories.click_repository import ClickRepository
from src.domain.repositories.date_repository import DateRepository
from src.domain.repositories.impression_repository import ImpressionRepository
from src.domain.repositories.ml_score_repository import MLScoreRepository


class AdServiceProtocol(Protocol):
    async def get_ad(self: Self, client: ClientEntity) -> CampaignAggregate | None: ...


class AdServiceImpl:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        ml_score_repository: MLScoreRepository,
        date_repository: DateRepository,
        impression_repository: ImpressionRepository,
        click_repository: ClickRepository,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.ml_score_repository = ml_score_repository
        self.date_repository = date_repository
        self.impression_repository = impression_repository
        self.click_repository = click_repository

    async def get_ad(self, client: ClientEntity) -> CampaignAggregate | None:
        current_date = await self.date_repository.get_current_date()

        campaigns = await self.campaign_repository.get_all_with_ml_scores(
            client.id, current_date
        )

        if not campaigns:
            return None

        max_ml_score = max(1, max(ml_score for _, ml_score in campaigns))

        campaign_stats = await self.campaign_repository.get_stats_by_id(
            [campaign.id for campaign, _ in campaigns]
        )

        IMPRESSION_SCORE_MULTIPLIER = 0.2
        CLICK_SCORE_MULTIPLIER = 0.01

        best_campaign = None
        best_score = float("-inf")

        for campaign, ml_score in campaigns:
            stats = campaign_stats.get(campaign.id, (0, 0))

            if stats[0] >= campaign.impressions_limit:
                continue

            score = (
                float(campaign.cost_per_click) * (ml_score / max_ml_score) * 0.7
                + float(campaign.cost_per_impression) * 0.4
            )

            if stats[0] > 0:
                score *= IMPRESSION_SCORE_MULTIPLIER
            if stats[1] > 0:
                score *= CLICK_SCORE_MULTIPLIER

            if score > best_score:
                best_score = score
                best_campaign = campaign

        return best_campaign


class AdServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        campaign_repository: CampaignRepository,
        ml_score_repository: MLScoreRepository,
        date_repository: DateRepository,
        impression_repository: ImpressionRepository,
        click_repository: ClickRepository,
    ) -> AdServiceProtocol:
        return AdServiceImpl(
            campaign_repository,
            ml_score_repository,
            date_repository,
            impression_repository,
            click_repository,
        )
