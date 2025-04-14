from typing import Protocol

from dishka import Provider, Scope, provide

from src.domain.repositories.date_repository import DateRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.schemas.time_schema import ITimeCreate, ITimeRead


class UpsertTimeUseCaseProtocol(Protocol):
    async def __call__(self, obj: ITimeCreate) -> ITimeRead: ...


class UpsertTimeUseCaseImpl:
    def __init__(self, date_repository: DateRepository) -> None:
        self.date_repository = date_repository

    async def __call__(self, obj: ITimeCreate) -> ITimeRead:
        date = await self.date_repository.get_current_date()
        if obj.current_date < date:
            raise DetailedHTTPException(ExceptionEnum.VALIDATION_ERROR)
        date = await self.date_repository.upsert_current_date(obj.current_date)
        return ITimeRead(current_date=date)


class UpsertTimeUseCaseUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        date_repository: DateRepository,
    ) -> UpsertTimeUseCaseProtocol:
        return UpsertTimeUseCaseImpl(date_repository)
