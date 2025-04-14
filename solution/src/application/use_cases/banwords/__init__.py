from src.application.use_cases.banwords.create_banwords_use_case import (
    CreateBanwordsUseCaseProvider,
)
from src.application.use_cases.banwords.delete_banwords_use_case import (
    DeleteBanwordsUseCaseProvider,
)
from src.application.use_cases.banwords.get_banwords_use_case import (
    GetBanwordsUseCaseProvider,
)

banwords_use_cases_providers = (
    CreateBanwordsUseCaseProvider(),
    DeleteBanwordsUseCaseProvider(),
    GetBanwordsUseCaseProvider(),
)
