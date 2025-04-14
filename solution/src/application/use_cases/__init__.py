from src.application.use_cases.ads import ads_use_cases_providers
from src.application.use_cases.advertisers import advertisers_use_cases_providers
from src.application.use_cases.banwords import banwords_use_cases_providers
from src.application.use_cases.bot import bot_use_cases_providers
from src.application.use_cases.campaigns import campaings_use_cases_providers
from src.application.use_cases.cdn import cdn_use_cases_providers
from src.application.use_cases.clients import clients_use_cases_providers
from src.application.use_cases.generate import generate_use_cases_providers
from src.application.use_cases.stats import stats_use_cases_providers
from src.application.use_cases.time import time_use_cases_providers

use_cases_providers = (
    *clients_use_cases_providers,
    *advertisers_use_cases_providers,
    *campaings_use_cases_providers,
    *stats_use_cases_providers,
    *time_use_cases_providers,
    *ads_use_cases_providers,
    *bot_use_cases_providers,
    *generate_use_cases_providers,
    *cdn_use_cases_providers,
    *banwords_use_cases_providers,
)
