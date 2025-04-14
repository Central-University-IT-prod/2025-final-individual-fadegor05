from src.application.use_cases.bot.get_campaign_use_case import (
    GetCampaignUseCaseProvider,
)
from src.application.use_cases.bot.get_campaigns_use_case import (
    GetCampaignsUseCaseProvider,
)
from src.application.use_cases.bot.get_start_use_case import GetStartUseCaseProvider
from src.application.use_cases.bot.get_stats_use_case import GetStatsUseCaseProvider

bot_use_cases_providers = (
    GetStartUseCaseProvider(),
    GetCampaignsUseCaseProvider(),
    GetCampaignUseCaseProvider(),
    GetStatsUseCaseProvider(),
)
