from typing import Self

from dishka import Provider, Scope, provide
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.aggregates.impression import ImpressionAggregate
from src.domain.repositories.impression_repository import ImpressionRepository
from src.infrastructure.db.models.impression_model import ImpressionModel
from src.infrastructure.db.repositories.event_repository_impl import EventRepositoryImpl


class ImpressionRepositoryImpl(
    EventRepositoryImpl[ImpressionAggregate, ImpressionModel], ImpressionRepository
):
    domain_type = ImpressionAggregate
    model_type = ImpressionModel

    async def _model_to_domain(
        self: Self, model: ImpressionModel
    ) -> ImpressionAggregate:
        return ImpressionAggregate(
            id=model.id,
            client_id=model.client_id,
            campaign_id=model.campaign_id,
            cost=model.cost,
            date=model.date,
        )

    async def _domain_to_model(
        self: Self, domain: ImpressionAggregate
    ) -> ImpressionModel:
        return ImpressionModel(
            id=domain.id,
            client_id=domain.client_id,
            campaign_id=domain.campaign_id,
            cost=domain.cost,
            date=domain.date,
        )


class ImpressionRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, session: AsyncSession) -> ImpressionRepository:
        return ImpressionRepositoryImpl(session)
