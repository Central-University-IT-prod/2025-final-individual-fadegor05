from typing import Protocol, Self

from dishka import Provider, Scope, provide

from src.core.settings import Settings
from src.domain.repositories.banword_repository import BanwordRepository
from src.infrastructure.adapters.ai_adapter import AIAdapterProtocol

MODERATION_PROMPT = """
Проведи анализ следующего текста и оцени его по множеству категорий возможных нарушений, из-за которых можно отказать в публикации рекламы на сайте крупного международного рекламного агенства.
Выведи результат в формате слова True или False
Где истина - пост прошел модерацию, а ложь, если содержит довольно много неприемлимого контента из этих категорий:
– нецензурные выражения, ругательства
– пошлый, эротический, непристойный контент
– разжигание ненависти, дискриминация
– упоминание наркотиков
– преступления, незаконные действия
– мошенничество, финансовые схемы
– оскорбления религии, верующих
– шокирующий, отталкивающий контент
– чрезмерная сексуализация, непристойные намёки
- унижение по расовому, половому или другому признаку

Будь объективным, но при этом не сильно строгим при оценивании, учитывай что контент может быть чуть-чуть провокационным
Ответ должен быть одним словом: True или False
"""


class ModerationServiceProtocol(Protocol):
    async def moderate_content_ai(self: Self, content: str) -> bool: ...

    async def moderate_content_banwords(self: Self, content: str) -> bool: ...

    async def moderate_content(self: Self, content: str) -> bool: ...


class ModerationServiceImpl:
    def __init__(
        self,
        settings: Settings,
        banword_repository: BanwordRepository,
        ai_adapter: AIAdapterProtocol,
    ) -> None:
        self.settings = settings
        self.banword_repository = banword_repository
        self.ai_adapter = ai_adapter

    async def moderate_content_ai(self: Self, content: str) -> bool:
        prompt = f"{MODERATION_PROMPT}\n\n{content}"
        result = await self.ai_adapter.send_message(prompt)
        if "True" in result:
            return True
        return False

    async def moderate_content_banwords(self: Self, content: str) -> bool:
        content = content.replace(" ", "").lower()
        banwords = await self.banword_repository.get_all_banwords_set()
        for banword in banwords:
            if banword in content:
                return False
        return True

    async def moderate_content(self: Self, content: str) -> bool:
        status = True
        if self.settings.moderation.banwords:
            status = status and await self.moderate_content_banwords(content)
        if self.settings.moderation.ai:
            status = status and await self.moderate_content_ai(content)
        return status


class ModerationServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        settings: Settings,
        banword_repository: BanwordRepository,
        ai_provider: AIAdapterProtocol,
    ) -> ModerationServiceProtocol:
        return ModerationServiceImpl(settings, banword_repository, ai_provider)
