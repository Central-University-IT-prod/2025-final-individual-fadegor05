from uuid import uuid4

from dishka import Provider, Scope, provide

from src.core.use_case import UseCaseProtocol
from src.domain.aggregates.ml_score import MLScoreAggregate
from src.domain.repositories.advertiser_repository import AdvertiserRepository
from src.domain.repositories.client_repository import ClientRepository
from src.domain.repositories.ml_score_repository import MLScoreRepository
from src.presentation.rest.exceptions import DetailedHTTPException, ExceptionEnum
from src.presentation.rest.schemas.ml_score_schema import IMLScoreRead

UpsertMLScoresUseCaseProtocol = UseCaseProtocol[None]


class UpsertMLScoresUseCaseImpl:
    def __init__(
        self,
        ml_score_repository: MLScoreRepository,
        advertiser_repository: AdvertiserRepository,
        client_repository: ClientRepository,
    ) -> None:
        self.ml_score_repository = ml_score_repository
        self.advertiser_repository = advertiser_repository
        self.client_repository = client_repository

    async def __call__(self, ml_score: IMLScoreRead) -> None:
        ml_score_domain = (
            await self.ml_score_repository.get_by_client_advertiser_ids_or_none(
                ml_score.client_id, ml_score.advertiser_id
            )
        )
        if ml_score_domain is None:
            client_domain = await self.client_repository.get_by_id_or_none(
                ml_score.client_id
            )
            advertiser_domain = await self.advertiser_repository.get_by_id_or_none(
                ml_score.advertiser_id
            )
            if client_domain is None or advertiser_domain is None:
                raise DetailedHTTPException(ExceptionEnum.NOT_FOUND)
            ml_score_domain = MLScoreAggregate(
                id=uuid4(),
                client_id=client_domain.id,
                advertiser_id=advertiser_domain.id,
                score=ml_score.score,
            )
        ml_score_domain.score = ml_score.score
        await self.ml_score_repository.update(ml_score_domain)


class UpsertMLScoresUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(
        self,
        ml_score_repository: MLScoreRepository,
        advertiser_repository: AdvertiserRepository,
        client_repository: ClientRepository,
    ) -> UpsertMLScoresUseCaseProtocol:
        return UpsertMLScoresUseCaseImpl(
            ml_score_repository,
            advertiser_repository,
            client_repository,
        )
