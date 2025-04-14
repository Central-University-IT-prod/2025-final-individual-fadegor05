from typing import Self
from uuid import uuid4

from dishka import Provider, Scope, provide
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.entities.date import DateEntity
from src.domain.repositories.date_repository import DateRepository
from src.infrastructure.db.models.date_model import DateModel
from src.infrastructure.db.repositories.base_repository_impl import BaseRepositoryImpl


class DateRepositoryImpl(BaseRepositoryImpl[DateEntity, DateModel], DateRepository):
    domain_type = DateEntity
    model_type = DateModel

    async def _model_to_domain(self: Self, model: DateModel) -> DateEntity:
        return DateEntity(id=model.id, date=model.date)

    async def _domain_to_model(self: Self, domain: DateEntity) -> DateModel:
        return DateModel(id=domain.id, date=domain.date)

    async def upsert_current_date(self: Self, date: int) -> int:
        query = select(self.model_type)
        model = (await self.session.exec(query)).one_or_none()
        if model is None:
            return (await self.create(DateEntity(id=uuid4(), date=date))).date
        model.date = date
        await self.session.commit()
        await self.session.refresh(model)
        return model.date

    async def get_current_date(self: Self) -> int:
        query = select(self.model_type)
        model = (await self.session.exec(query)).one_or_none()
        if model is None:
            return await self.upsert_current_date(0)
        return model.date

    async def increment_current_date(self: Self) -> int:
        current_date = await self.get_current_date()
        return await self.upsert_current_date(current_date + 1)


class DateRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, session: AsyncSession) -> DateRepository:
        return DateRepositoryImpl(session)
