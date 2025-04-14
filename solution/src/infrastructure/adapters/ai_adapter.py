from typing import Protocol, Self

import aiohttp
from dishka import Provider, Scope, provide

from src.core.settings import Settings


class AIAdapterProtocol(Protocol):
    async def send_message(self: Self, prompt: str) -> str: ...


class AIAdapterImpl:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def send_message(self: Self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.settings.openrouter.token}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                },
            ) as response:
                return (await response.json())["choices"][0]["message"]["content"]


class AIAdapterProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, settings: Settings) -> AIAdapterProtocol:
        return AIAdapterImpl(settings)
