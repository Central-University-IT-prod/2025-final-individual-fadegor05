from typing import Protocol, TypeVar

UseCaseResultType = TypeVar("UseCaseResultType", covariant=True)


class UseCaseProtocol(Protocol[UseCaseResultType]):
    async def __call__(self, *args: any, **kwargs: any) -> UseCaseResultType: ...  # type: ignore
