from src.application.use_cases.stats.get_advertiser_stats_daily_use_case import (
    GetAdvertiserStatsDailyUseCaseProvider,
)
from src.application.use_cases.stats.get_advertiser_stats_use_case import (
    GetAdvertiserStatsUseCaseProvider,
)
from src.application.use_cases.stats.get_campaign_stats_daily_use_case import (
    GetCampaignStatsDailyUseCaseProvider,
)
from src.application.use_cases.stats.get_campaign_stats_use_case import (
    GetCampaignStatsUseCaseProvider,
)

stats_use_cases_providers = (
    GetCampaignStatsDailyUseCaseProvider(),
    GetCampaignStatsUseCaseProvider(),
    GetAdvertiserStatsDailyUseCaseProvider(),
    GetAdvertiserStatsUseCaseProvider(),
)
