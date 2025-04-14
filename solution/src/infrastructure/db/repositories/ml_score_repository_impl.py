from typing import Self
from uuid import UUID

from dishka import Provider, Scope, provide
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.aggregates.ml_score import MLScoreAggregate
from src.domain.repositories.ml_score_repository import MLScoreRepository
from src.infrastructure.db.models.ml_score_model import MLScoreModel
from src.infrastructure.db.repositories.base_repository_impl import BaseRepositoryImpl


class MLScoreRepositoryImpl(
    BaseRepositoryImpl[MLScoreAggregate, MLScoreModel], MLScoreRepository
):
    domain_type = MLScoreAggregate
    model_type = MLScoreModel

    async def _model_to_domain(self: Self, model: MLScoreModel) -> MLScoreAggregate:
        return MLScoreAggregate(
            id=model.id,
            client_id=model.client_id,
            advertiser_id=model.advertiser_id,
            score=model.score,
        )

    async def _domain_to_model(self: Self, domain: MLScoreAggregate) -> MLScoreModel:
        return MLScoreModel(
            id=domain.id,
            client_id=domain.client_id,
            advertiser_id=domain.advertiser_id,
            score=domain.score,
        )

    async def get_by_client_advertiser_ids_or_none(
        self: Self, client_id: UUID, advertiser_id: UUID
    ) -> MLScoreAggregate | None:
        query = select(self.model_type).where(
            and_(
                self.model_type.client_id == client_id,
                self.model_type.advertiser_id == advertiser_id,
            )
        )
        result = (await self.session.exec(query)).one_or_none()
        if result is None:
            return None
        return await self._model_to_domain(result)

    async def get_by_client_advertiser_ids(
        self: Self, client_id: UUID, advertiser_ids: list[UUID]
    ) -> list[MLScoreAggregate]:
        if not advertiser_ids:
            return []

        query = select(self.model_type).where(
            and_(
                self.model_type.client_id == client_id,
                self.model_type.advertiser_id.in_(advertiser_ids),  # type: ignore
            )
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]


class MLScoreRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, session: AsyncSession) -> MLScoreRepository:
        return MLScoreRepositoryImpl(session)
