from typing import Self, TypeVar
from uuid import UUID

from sqlmodel import and_, func, select

from src.domain.base import BaseDomain
from src.domain.repositories.event_repository import EventRepository
from src.infrastructure.db.models.base_model import BaseModel
from src.infrastructure.db.models.campaign_model import CampaignModel
from src.infrastructure.db.repositories.base_repository_impl import BaseRepositoryImpl

EventDomainType = TypeVar("EventDomainType", bound=BaseDomain)
EventModelType = TypeVar("EventModelType", bound=BaseModel)


class EventRepositoryImpl(
    BaseRepositoryImpl[EventDomainType, EventModelType],
    EventRepository,
):
    async def get_all_by_campaign_id(
        self: Self, campaign_id: UUID
    ) -> list[EventDomainType]:
        query = (
            select(self.model_type)
            .where(self.model_type.campaign_id == campaign_id)  # type: ignore
            .order_by(self.model_type.date)  # type: ignore
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def get_all_by_campaign_id_and_date(
        self: Self, campaign_id: UUID, date: int
    ) -> list[EventDomainType]:
        query = (
            select(self.model_type)
            .where(
                and_(
                    self.model_type.campaign_id == campaign_id,  # type: ignore
                    self.model_type.date == date,  # type: ignore
                )
            )
            .order_by(self.model_type.date)  # type: ignore
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def get_all_by_advertiser_id(
        self: Self, advertiser_id: UUID
    ) -> list[EventDomainType]:
        query = (
            select(self.model_type)
            .join(CampaignModel)
            .where(CampaignModel.advertiser_id == advertiser_id)
            .order_by(self.model_type.date)  # type: ignore
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def get_all_by_advertiser_id_and_date(
        self: Self, advertiser_id: UUID, date: int
    ) -> list[EventDomainType]:
        query = (
            select(self.model_type)
            .join(CampaignModel)
            .where(
                and_(
                    CampaignModel.advertiser_id == advertiser_id,
                    self.model_type.date == date,  # type: ignore
                )
            )
            .order_by(self.model_type.date)  # type: ignore
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def get_by_campaign_id_and_client_id_or_none(
        self: Self, campaign_id: UUID, client_id: UUID
    ) -> EventDomainType | None:
        query = select(self.model_type).where(
            and_(
                self.model_type.campaign_id == campaign_id,  # type: ignore
                self.model_type.client_id == client_id,  # type: ignore
            )
        )
        result = (await self.session.exec(query)).one_or_none()
        if result is None:
            return None
        return await self._model_to_domain(result)

    async def get_amount_by_campaign_id(self: Self, campaign_id: UUID) -> int:
        query = select(self.model_type).where(
            self.model_type.campaign_id == campaign_id,  # type: ignore
        )
        count_query = select(func.count()).select_from(query)  # type: ignore
        amount = (await self.session.exec(count_query)).first()
        amount = amount if amount is not None else 0
        return amount

    async def get_by_campaign_ids_and_client_id(
        self: Self, campaign_ids: list[UUID], client_id: UUID
    ) -> list[EventDomainType]:
        if not campaign_ids:
            return []

        query = (
            select(self.model_type)
            .where(
                and_(
                    self.model_type.campaign_id.in_(campaign_ids),  # type: ignore
                    self.model_type.client_id == client_id,  # type: ignore
                )
            )
            .order_by(self.model_type.date)  # type: ignore
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def get_amount_by_campaign_ids(
        self: Self, campaign_ids: list[UUID]
    ) -> dict[UUID, int]:
        if not campaign_ids:
            return {}

        query = (
            select(self.model_type.campaign_id, func.count().label("amount"))  # type: ignore
            .where(self.model_type.campaign_id.in_(campaign_ids))  # type: ignore
            .group_by(self.model_type.campaign_id)  # type: ignore
        )
        result = (await self.session.exec(query)).all()

        return {campaign_id: amount for campaign_id, amount in result}
