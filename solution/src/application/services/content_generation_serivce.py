from typing import Protocol, Self

from dishka import Provider, Scope, provide

from src.infrastructure.adapters.ai_adapter import AIAdapterProtocol

TEXT_GENERATION_PROMT = """
Представь, что ты профессиональный рекламный аналитик с многолетним опытом, тебе нужно составить цепкий, интересный, молодежный текст рекламного поста (3-4 предложения, не используй эмодзи), по его заголовку и названию рекламодателя, твоим ответом должен быть только рекламный текст
"""


class ContentGenerationServiceProtocol(Protocol):
    async def generate_text(self: Self, title: str, advertiser_name: str) -> str: ...


class ContentGenerationServiceImpl:
    def __init__(
        self,
        ai_adapter: AIAdapterProtocol,
    ) -> None:
        self.ai_adapter = ai_adapter

    async def generate_text(self: Self, title: str, advertiser_name: str) -> str:
        text = await self.ai_adapter.send_message(
            f"{TEXT_GENERATION_PROMT}\n\n{title}\n{advertiser_name}"
        )
        return text.replace("\n", "")


class ContentGenerationServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        ai_adapter: AIAdapterProtocol,
    ) -> ContentGenerationServiceProtocol:
        return ContentGenerationServiceImpl(ai_adapter)
