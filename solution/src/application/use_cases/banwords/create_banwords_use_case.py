from typing import Protocol
from uuid import uuid4

from dishka import Provider, Scope, provide

from src.domain.entities.banword import BanwordEntity
from src.domain.repositories.banword_repository import BanwordRepository


class CreateBanwordsUseCaseProtocol(Protocol):
    async def __call__(self, objs: list[str]) -> list[str]: ...


class CreateBanwordsUseCaseImpl:
    def __init__(self, banword_repository: BanwordRepository) -> None:
        self.banword_repository = banword_repository

    async def __call__(self, objs: list[str]) -> list[str]:
        banwords_added: list[str] = []
        for obj in objs:
            banword = await self.banword_repository.get_by_word_or_none(obj.lower())
            if banword is None:
                banword = await self.banword_repository.create(
                    BanwordEntity(id=uuid4(), word=obj.lower())
                )
                banwords_added.append(banword.word)
        return banwords_added


class CreateBanwordsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self, banword_repository: BanwordRepository
    ) -> CreateBanwordsUseCaseProtocol:
        return CreateBanwordsUseCaseImpl(banword_repository)
