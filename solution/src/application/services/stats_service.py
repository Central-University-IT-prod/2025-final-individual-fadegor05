from decimal import Decimal
from typing import Protocol

from dishka import Provider, Scope, provide

from src.domain.aggregates.campaign import CampaignAggregate
from src.domain.aggregates.click import ClickAggregate
from src.domain.aggregates.impression import ImpressionAggregate
from src.domain.entities.advertiser import AdvertiserEntity
from src.domain.repositories.click_repository import ClickRepository
from src.domain.repositories.date_repository import DateRepository
from src.domain.repositories.impression_repository import ImpressionRepository
from src.domain.value_objects.stats import Stats, StatsDaily


class StatsServiceProtocol(Protocol):
    async def get_stats_by_campaign(self, campaign: CampaignAggregate) -> Stats: ...

    async def get_stats_daily_by_campaign(
        self, campaign: CampaignAggregate
    ) -> list[StatsDaily]: ...

    async def get_stats_by_advertiser(self, advertiser: AdvertiserEntity) -> Stats: ...

    async def get_stats_daily_by_advertiser(
        self, advertiser: AdvertiserEntity
    ) -> list[StatsDaily]: ...


class StatsServiceImpl:
    def __init__(
        self,
        click_repository: ClickRepository,
        impression_repository: ImpressionRepository,
        date_repository: DateRepository,
    ) -> None:
        self.click_repository = click_repository
        self.impression_repository = impression_repository
        self.date_repository = date_repository

    def _to_stats(
        self,
        clicks: list[ClickAggregate],
        impressions: list[ImpressionAggregate],
    ) -> Stats:
        impressions_count = len(impressions)
        clicks_count = len(clicks)
        conversion = 0
        if impressions_count != 0:
            conversion = (clicks_count / impressions_count) * 100
        spent_impressions = Decimal(0)
        for impression in impressions:
            spent_impressions += impression.cost
        spent_clicks = Decimal(0)
        for click in clicks:
            spent_clicks += click.cost
        return Stats(
            impressions_count=impressions_count,
            clicks_count=clicks_count,
            conversion=conversion,
            spent_impressions=spent_impressions,
            spent_clicks=spent_clicks,
            spent_total=spent_clicks + spent_impressions,
        )

    def _to_stats_daily(
        self,
        clicks: list[ClickAggregate],
        impressions: list[ImpressionAggregate],
        date: int,
    ) -> StatsDaily:
        stats = self._to_stats(clicks, impressions)
        return StatsDaily(
            impressions_count=stats.impressions_count,
            clicks_count=stats.clicks_count,
            conversion=stats.conversion,
            spent_impressions=stats.spent_impressions,
            spent_clicks=stats.spent_clicks,
            spent_total=stats.spent_total,
            date=date,
        )

    async def get_stats_by_campaign(self, campaign: CampaignAggregate) -> Stats:
        clicks = await self.click_repository.get_all_by_campaign_id(
            campaign_id=campaign.id
        )
        impressions = await self.impression_repository.get_all_by_campaign_id(
            campaign_id=campaign.id
        )
        return self._to_stats(clicks, impressions)

    async def get_stats_daily_by_campaign(
        self, campaign: CampaignAggregate
    ) -> list[StatsDaily]:
        max_day = await self.date_repository.get_current_date()
        stats_daily: list[StatsDaily] = []
        for date in range(max_day + 1):
            clicks = await self.click_repository.get_all_by_campaign_id_and_date(
                campaign.id, date
            )
            impressions = (
                await self.impression_repository.get_all_by_campaign_id_and_date(
                    campaign.id, date
                )
            )
            stats_daily.append(self._to_stats_daily(clicks, impressions, date))
        return stats_daily

    async def get_stats_by_advertiser(self, advertiser: AdvertiserEntity) -> Stats:
        clicks = await self.click_repository.get_all_by_advertiser_id(advertiser.id)
        impressions = await self.impression_repository.get_all_by_advertiser_id(
            advertiser.id
        )
        return self._to_stats(clicks, impressions)

    async def get_stats_daily_by_advertiser(
        self, advertiser: AdvertiserEntity
    ) -> list[StatsDaily]:
        max_day = await self.date_repository.get_current_date()
        stats_daily: list[StatsDaily] = []
        for date in range(max_day + 1):
            clicks = await self.click_repository.get_all_by_advertiser_id_and_date(
                advertiser.id, date
            )
            impressions = (
                await self.impression_repository.get_all_by_advertiser_id_and_date(
                    advertiser.id, date
                )
            )
            stats_daily.append(self._to_stats_daily(clicks, impressions, date))
        return stats_daily


class StatsServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        click_repository: ClickRepository,
        impression_repository: ImpressionRepository,
        date_repository: DateRepository,
    ) -> StatsServiceProtocol:
        return StatsServiceImpl(
            click_repository,
            impression_repository,
            date_repository,
        )
