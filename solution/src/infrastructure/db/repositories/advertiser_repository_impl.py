from typing import Self

from dishka import Provider, Scope, provide
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.entities.advertiser import AdvertiserEntity
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.infrastructure.db.models.advertiser_model import AdvertiserModel
from src.infrastructure.db.repositories.base_repository_impl import BaseRepositoryImpl


class AdvertiserRepositoryImpl(
    BaseRepositoryImpl[AdvertiserEntity, AdvertiserModel], AdvertiserRepository
):
    domain_type = AdvertiserEntity
    model_type = AdvertiserModel

    async def _model_to_domain(self: Self, model: AdvertiserModel) -> AdvertiserEntity:
        return AdvertiserEntity(
            id=model.id,
            telegram_id=model.telegram_id,
            name=model.name,
        )

    async def _domain_to_model(self: Self, domain: AdvertiserEntity) -> AdvertiserModel:
        return AdvertiserModel(
            id=domain.id,
            telegram_id=domain.telegram_id,
            name=domain.name,
        )

    async def get_by_telegram_id_or_none(
        self: Self, telegram_id: int
    ) -> AdvertiserEntity | None:
        async with self.session as s:
            query = select(self.model_type).where(
                self.model_type.telegram_id == telegram_id
            )
            result = (await s.exec(query)).one_or_none()
            if result is None:
                return None
            return await self._model_to_domain(result)


class AdvertiserRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, session: AsyncSession) -> AdvertiserRepository:
        return AdvertiserRepositoryImpl(session)
