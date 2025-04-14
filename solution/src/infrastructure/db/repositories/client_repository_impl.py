from typing import Self

from dishka import Provider, Scope, provide
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.entities.client import ClientEntity
from src.domain.repositories.client_repository import ClientRepository
from src.infrastructure.db.models.client_model import ClientModel
from src.infrastructure.db.repositories.base_repository_impl import BaseRepositoryImpl


class ClientRepositoryImpl(
    BaseRepositoryImpl[ClientEntity, ClientModel], ClientRepository
):
    domain_type = ClientEntity
    model_type = ClientModel

    async def _model_to_domain(self: Self, model: ClientModel) -> ClientEntity:
        return ClientEntity(
            id=model.id,
            login=model.login,
            age=model.age,
            location=model.location,
            gender=model.gender,
        )

    async def _domain_to_model(self: Self, domain: ClientEntity) -> ClientModel:
        return ClientModel(
            id=domain.id,
            login=domain.login,
            age=domain.age,
            location=domain.location,
            gender=domain.gender,
        )


class ClientRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, session: AsyncSession) -> ClientRepository:
        return ClientRepositoryImpl(session)
