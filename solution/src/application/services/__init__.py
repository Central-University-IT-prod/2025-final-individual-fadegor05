from src.application.services.ad_service import AdServiceProvider
from src.application.services.content_generation_serivce import (
    ContentGenerationServiceProvider,
)
from src.application.services.moderation_service import ModerationServiceProvider
from src.application.services.stats_service import StatsServiceProvider
from src.application.services.telegram_auth_service import TelegramAuthServiceProvider

services_providers = (
    StatsServiceProvider(),
    AdServiceProvider(),
    TelegramAuthServiceProvider(),
    ModerationServiceProvider(),
    ContentGenerationServiceProvider(),
)
