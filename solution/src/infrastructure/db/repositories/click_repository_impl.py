from typing import Self

from dishka import Provider, Scope, provide
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.aggregates.click import ClickAggregate
from src.domain.repositories.click_repository import ClickRepository
from src.infrastructure.db.models.click_model import ClickModel
from src.infrastructure.db.repositories.event_repository_impl import EventRepositoryImpl


class ClickRepositoryImpl(
    EventRepositoryImpl[ClickAggregate, ClickModel], ClickRepository
):
    domain_type = ClickAggregate
    model_type = ClickModel

    async def _model_to_domain(self: Self, model: ClickModel) -> ClickAggregate:
        return ClickAggregate(
            id=model.id,
            client_id=model.client_id,
            campaign_id=model.campaign_id,
            cost=model.cost,
            date=model.date,
        )

    async def _domain_to_model(self: Self, domain: ClickAggregate) -> ClickModel:
        return ClickModel(
            id=domain.id,
            client_id=domain.client_id,
            campaign_id=domain.campaign_id,
            cost=domain.cost,
            date=domain.date,
        )


class ClickRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, session: AsyncSession) -> ClickRepository:
        return ClickRepositoryImpl(session)
