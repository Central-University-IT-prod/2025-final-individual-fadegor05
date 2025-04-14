from dishka import Provider, Scope, provide
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.entities.banword import BanwordEntity
from src.domain.repositories.banword_repository import BanwordRepository
from src.infrastructure.db.models.banword_model import BanwordModel
from src.infrastructure.db.repositories.base_repository_impl import BaseRepositoryImpl


class BanwordRepositoryImpl(
    BaseRepositoryImpl[BanwordEntity, BanwordModel], BanwordRepository
):
    domain_type = BanwordEntity
    model_type = BanwordModel

    async def _model_to_domain(self, model: BanwordModel) -> BanwordEntity:
        return BanwordEntity(
            id=model.id,
            word=model.word,
        )

    async def _domain_to_model(self, domain: BanwordEntity) -> BanwordModel:
        return BanwordModel(
            id=domain.id,
            word=domain.word,
        )

    async def get_by_word_or_none(self, word: str) -> BanwordEntity | None:
        query = select(self.model_type).where(self.model_type.word == word)
        result = (await self.session.exec(query)).one_or_none()
        if result is None:
            return None
        return await self._model_to_domain(result)

    async def get_all_banwords_set(self) -> set[str]:
        query = select(self.model_type)
        result = (await self.session.exec((query))).all()
        return set(model.word for model in result)


class BanwordRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, session: AsyncSession) -> BanwordRepository:
        return BanwordRepositoryImpl(session)
