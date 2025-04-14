from src.application.use_cases.ads.click_ad_use_case import ClickAdUseCaseProvider
from src.application.use_cases.ads.get_ad_use_case import (
    GetAdUseCaseProvider,
)

ads_use_cases_providers = (
    ClickAdUseCaseProvider(),
    GetAdUseCaseProvider(),
)
