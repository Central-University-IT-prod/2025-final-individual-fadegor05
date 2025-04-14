from abc import ABC, abstractmethod
from typing import Generic, Self, TypeVar
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.pagination import Pagination
from src.domain.base import BaseDomain
from src.domain.repositories.base_repository import BaseRepository
from src.infrastructure.db.models.base_model import BaseModel

DomainType = TypeVar("DomainType", bound=BaseDomain)
ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepositoryImpl(
    ABC, Generic[DomainType, ModelType], BaseRepository[DomainType]
):
    domain_type: type[DomainType]
    model_type: type[ModelType]

    def __init__(self: Self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    async def _model_to_domain(self: Self, model: ModelType) -> DomainType: ...

    @abstractmethod
    async def _domain_to_model(self: Self, domain: DomainType) -> ModelType: ...

    async def get_by_id_or_none(self: Self, id: UUID) -> DomainType | None:
        query = select(self.model_type).where(self.model_type.id == id)
        result = (await self.session.exec(query)).one_or_none()
        if result is None:
            return None
        return await self._model_to_domain(result)

    async def get_paginated(self: Self, pagination: Pagination) -> list[DomainType]:
        query = (
            select(self.model_type).limit(pagination.limit).offset(pagination.offset)
        )
        result = (await self.session.exec(query)).all()
        return [await self._model_to_domain(model) for model in result]

    async def create(self: Self, obj: DomainType) -> DomainType:
        model = await self._domain_to_model(obj)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return await self._model_to_domain(model)

    async def bulk_create(
        self: Self, objs: list[DomainType]
    ) -> list[DomainType] | None:
        models: list[ModelType] = [await self._domain_to_model(obj) for obj in objs]
        try:
            self.session.add_all(models)
            await self.session.commit()
            for model in models:
                await self.session.refresh(model)
            return [await self._model_to_domain(obj) for obj in models]
        except:
            return None

    async def update(self: Self, obj: DomainType) -> DomainType:
        model = await self._domain_to_model(obj)
        model = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(model)
        return await self._model_to_domain(model)

    async def bulk_update(self: Self, objs: list[DomainType]) -> list[DomainType]:
        models: list[ModelType] = []
        for obj in objs:
            model = await self._domain_to_model(obj)
            model = await self.session.merge(model)
            models.append(model)
        await self.session.commit()
        for model in models:
            await self.session.refresh(model)
        return [await self._model_to_domain(obj) for obj in models]

    async def delete(self: Self, id: UUID) -> None:
        query = select(self.model_type).where(self.model_type.id == id)
        result = (await self.session.exec(query)).one_or_none()
        if result is None:
            return None
        await self.session.delete(result)
        await self.session.commit()
