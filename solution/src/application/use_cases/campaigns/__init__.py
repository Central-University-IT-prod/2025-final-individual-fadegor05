from src.application.use_cases.campaigns.create_campaign_use_case import (
    CreateCampaignUseCaseProvider,
)
from src.application.use_cases.campaigns.delete_campaign_image_use_case import (
    DeleteCampaignImageUseCaseProvider,
)
from src.application.use_cases.campaigns.delete_campaign_use_case import (
    DeleteCampaignUseCaseProvider,
)
from src.application.use_cases.campaigns.get_campaign_use_case import (
    GetCampaignUseCaseProvider,
)
from src.application.use_cases.campaigns.get_campaigns_use_case import (
    GetCampaignsUseCaseProvider,
)
from src.application.use_cases.campaigns.update_campaign_use_case import (
    UpdateCampaignUseCaseProvider,
)
from src.application.use_cases.campaigns.upload_campaign_image_use_case import (
    UploadCampaignImageUseCaseProvider,
)

campaings_use_cases_providers = (
    CreateCampaignUseCaseProvider(),
    DeleteCampaignUseCaseProvider(),
    GetCampaignsUseCaseProvider(),
    GetCampaignUseCaseProvider(),
    UpdateCampaignUseCaseProvider(),
    UploadCampaignImageUseCaseProvider(),
    DeleteCampaignImageUseCaseProvider(),
)
