from typing import Protocol

from dishka import Provider, Scope, provide

from src.domain.repositories.banword_repository import BanwordRepository


class GetBanwordsUseCaseProtocol(Protocol):
    async def __call__(self) -> list[str]: ...


class GetBanwordsUseCaseImpl:
    def __init__(self, banword_repository: BanwordRepository) -> None:
        self.banword_repository = banword_repository

    async def __call__(self) -> list[str]:
        return list(await self.banword_repository.get_all_banwords_set())


class GetBanwordsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self, banword_repository: BanwordRepository
    ) -> GetBanwordsUseCaseProtocol:
        return GetBanwordsUseCaseImpl(banword_repository)
