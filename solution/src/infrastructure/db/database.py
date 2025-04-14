from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.settings import Settings


class AsyncSessionProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self, settings: Settings) -> AsyncEngine:
        gunicorn_workers = settings.gunicorn.workers
        connections_per_worker = 4
        pool_size = gunicorn_workers * connections_per_worker
        max_overflow = pool_size

        return create_async_engine(
            settings.postgres.url,
            echo=False,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
            pool_timeout=90,
            pool_recycle=3600,
            pool_use_lifo=True,
        )

    @provide(scope=Scope.REQUEST)
    async def session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        async with AsyncSession(engine) as session:
            yield session
