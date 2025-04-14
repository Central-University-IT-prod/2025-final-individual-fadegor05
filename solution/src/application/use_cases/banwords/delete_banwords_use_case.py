from typing import Protocol

from dishka import Provider, Scope, provide

from src.domain.repositories.banword_repository import BanwordRepository


class DeleteBanwordsUseCaseProtocol(Protocol):
    async def __call__(self, objs: list[str]) -> list[str]: ...


class DeleteBanwordsUseCaseImpl:
    def __init__(self, banword_repository: BanwordRepository) -> None:
        self.banword_repository = banword_repository

    async def __call__(self, objs: list[str]) -> list[str]:
        banwords_deleted: list[str] = []
        for obj in objs:
            banword = await self.banword_repository.get_by_word_or_none(obj.lower())
            if banword is not None:
                await self.banword_repository.delete(banword.id)
                banwords_deleted.append(banword.word)
        return banwords_deleted


class DeleteBanwordsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        banword_repository: BanwordRepository,
    ) -> DeleteBanwordsUseCaseProtocol:
        return DeleteBanwordsUseCaseImpl(banword_repository)
