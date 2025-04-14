from src.application.use_cases.advertisers.create_advertisers_use_case import (
    CreateAdvertisersUseCaseProvider,
)
from src.application.use_cases.advertisers.get_advertiser_use_case import (
    GetAdvertiserUseCaseProvider,
)
from src.application.use_cases.advertisers.upsert_ml_scores_use_case import (
    UpsertMLScoresUseCaseProvider,
)

advertisers_use_cases_providers = (
    CreateAdvertisersUseCaseProvider(),
    GetAdvertiserUseCaseProvider(),
    UpsertMLScoresUseCaseProvider(),
)
