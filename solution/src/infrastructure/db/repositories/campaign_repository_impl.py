from typing import Self
from uuid import UUID

from dishka import Provider, Scope, provide
from sqlmodel import VARCHAR, and_, cast, func, or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.enums import AllGenderEnum
from src.core.pagination import Pagination
from src.domain.aggregates.campaign import CampaignAggregate
from src.domain.entities.client import ClientEntity
from src.domain.repositories.campaign_repository import CampaignRepository
from src.domain.value_objects.targeting import Targeting
from src.infrastructure.db.models.advertiser_model import AdvertiserModel
from src.infrastructure.db.models.campaign_model import CampaignModel
from src.infrastructure.db.models.client_model import ClientModel
from src.infrastructure.db.models.ml_score_model import MLScoreModel
from src.infrastructure.db.repositories.base_repository_impl import BaseRepositoryImpl


class CampaignRepositoryImpl(
    BaseRepositoryImpl[CampaignAggregate, CampaignModel], CampaignRepository
):
    domain_type = CampaignAggregate
    model_type = CampaignModel

    async def get_by_id_or_none(self: Self, id: UUID) -> CampaignAggregate | None:
        campaign = await super().get_by_id_or_none(id)
        if campaign is not None and campaign.hide:
            return None
        return campaign

    async def _model_to_domain(self: Self, model: CampaignModel) -> CampaignAggregate:
        await self.session.refresh(model)
        return CampaignAggregate(
            id=model.id,
            cost_per_impression=model.cost_per_impression,
            cost_per_click=model.cost_per_click,
            ad_title=model.ad_title,
            ad_text=model.ad_text,
            impressions_limit=model.impressions_limit,
            clicks_limit=model.clicks_limit,
            start_date=model.start_date,
            end_date=model.end_date,
            hide=model.hide,
            targeting=Targeting(
                gender=model.gender,
                age_from=model.age_from,
                age_to=model.age_to,
                location=model.location,
            ),
            image=model.image,
            advertiser_id=model.advertiser_id,
        )

    async def _domain_to_model(self: Self, domain: CampaignAggregate) -> CampaignModel:
        return CampaignModel(
            id=domain.id,
            cost_per_impression=domain.cost_per_impression,
            cost_per_click=domain.cost_per_click,
            ad_title=domain.ad_title,
            ad_text=domain.ad_text,
            impressions_limit=domain.impressions_limit,
            clicks_limit=domain.clicks_limit,
            start_date=domain.start_date,
            end_date=domain.end_date,
            hide=domain.hide,
            gender=domain.targeting.gender if domain.targeting is not None else None,
            age_from=domain.targeting.age_from
            if domain.targeting is not None
            else None,
            age_to=domain.targeting.age_to if domain.targeting is not None else None,
            location=domain.targeting.location
            if domain.targeting is not None
            else None,
            image=domain.image,
            advertiser_id=domain.advertiser_id,
        )

    async def get_paginated_by_advertiser_id(
        self: Self, pagination: Pagination, advertiser_id: UUID
    ) -> list[CampaignAggregate]:
        query = (
            select(self.model_type)
            .where(self.model_type.advertiser_id == advertiser_id)
            .where(self.model_type.hide == False)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def get_all_targeting_client(
        self: Self, client: ClientEntity, current_date: int
    ) -> list[CampaignAggregate]:
        query = (
            select(self.model_type)
            .where(self.model_type.start_date <= current_date)
            .where(self.model_type.end_date >= current_date)
            .where(self.model_type.hide == False)
            .where(func.coalesce(self.model_type.age_from, 0) <= client.age)
            .where(func.coalesce(self.model_type.age_to, 2147483647) >= client.age)
            .where(
                func.coalesce(self.model_type.location, client.location)
                == client.location
            )
            .where(
                or_(
                    func.coalesce(self.model_type.gender, client.gender)
                    == client.gender,
                    self.model_type.gender == AllGenderEnum.ALL,
                )
            )
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def get_all_by_advertiser_id(
        self: Self, advertiser_id: UUID
    ) -> list[CampaignAggregate]:
        query = (
            select(self.model_type)
            .where(self.model_type.advertiser_id == advertiser_id)
            .where(self.model_type.hide == False)
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def hide(self: Self, campaign_id: UUID) -> None:
        query = select(self.model_type).where(self.model_type.id == campaign_id)
        model = (await self.session.exec(query)).one_or_none()
        if model is None:
            return None
        model.hide = True
        await self.session.commit()

    async def get_all_with_ml_scores(
        self: Self, client_id: UUID, current_date: int
    ) -> list[tuple[CampaignAggregate, int]]:
        query = (
            select(self.model_type, MLScoreModel.score)
            .join(AdvertiserModel, AdvertiserModel.id == self.model_type.advertiser_id)  # type: ignore
            .outerjoin(
                MLScoreModel,
                and_(
                    MLScoreModel.advertiser_id == AdvertiserModel.id,
                    MLScoreModel.client_id == client_id,
                ),
            )
            .outerjoin(ClientModel, and_(ClientModel.id == client_id))
            .where(self.model_type.start_date <= current_date)
            .where(self.model_type.end_date >= current_date)
            .where(self.model_type.hide == False)
            .where(func.coalesce(self.model_type.age_from, 0) <= ClientModel.age)
            .where(func.coalesce(self.model_type.age_to, 2147483647) >= ClientModel.age)
            .where(
                func.coalesce(self.model_type.location, ClientModel.location)
                == ClientModel.location
            )
            .where(
                or_(
                    self.model_type.gender.is_(None),  # type: ignore
                    cast(self.model_type.gender, VARCHAR)
                    == cast(ClientModel.gender, VARCHAR),
                    self.model_type.gender == AllGenderEnum.ALL,
                )
            )
        )

        result = (await self.session.exec(query)).all()

        campaigns_with_scores = []
        for campaign, score in result:
            campaign_aggregate = await self._model_to_domain(campaign)
            campaigns_with_scores.append((campaign_aggregate, score or 0))

        return campaigns_with_scores

    async def get_stats_by_id(
        self: Self, campaign_ids: list[UUID]
    ) -> dict[UUID, tuple[int, int]]:
        query = (
            select(self.model_type).where(self.model_type.id.in_(campaign_ids))  # type: ignore
        )
        result = (await self.session.exec(query)).all()
        return {
            model.id: (len(model.impressions), len(model.clicks)) for model in result
        }


class CampaignRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, session: AsyncSession) -> CampaignRepository:
        return CampaignRepositoryImpl(session)
