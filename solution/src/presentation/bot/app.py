import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import (
    setup_dishka,
)

from src.core.providers import create_async_container, get_providers
from src.core.settings import Settings
from src.presentation.bot.dialogs import dialogs
from src.presentation.bot.handlers.router import router


async def bot() -> None:
    defaults = DefaultBotProperties(parse_mode="Markdown")
    providers = get_providers()
    container = create_async_container(providers)
    settings = await container.get(Settings)
    bot = Bot(token=settings.bot.token, default=defaults)
    dp = Dispatcher()
    dp.include_routers(router, *dialogs())
    setup_dialogs(dp)

    setup_dishka(container=container, router=dp, auto_inject=True)
    await dp.start_polling(bot)  # type: ignore


def startup_bot() -> None:
    asyncio.run(bot())


if __name__ == "__main__":
    startup_bot()
