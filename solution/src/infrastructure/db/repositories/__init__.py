from src.infrastructure.db.repositories.advertiser_repository_impl import (
    AdvertiserRepositoryProvider,
)
from src.infrastructure.db.repositories.banword_repository_impl import (
    BanwordRepositoryProvider,
)
from src.infrastructure.db.repositories.campaign_repository_impl import (
    CampaignRepositoryProvider,
)
from src.infrastructure.db.repositories.click_repository_impl import (
    ClickRepositoryProvider,
)
from src.infrastructure.db.repositories.client_repository_impl import (
    ClientRepositoryProvider,
)
from src.infrastructure.db.repositories.date_repository_impl import (
    DateRepositoryProvider,
)
from src.infrastructure.db.repositories.impression_repository_impl import (
    ImpressionRepositoryProvider,
)
from src.infrastructure.db.repositories.ml_score_repository_impl import (
    MLScoreRepositoryProvider,
)

repositories_providers = (
    AdvertiserRepositoryProvider(),
    ClientRepositoryProvider(),
    CampaignRepositoryProvider(),
    MLScoreRepositoryProvider(),
    ClickRepositoryProvider(),
    ImpressionRepositoryProvider(),
    DateRepositoryProvider(),
    BanwordRepositoryProvider(),
)
