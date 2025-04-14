from src.infrastructure.adapters.ai_adapter import AIAdapterProvider
from src.infrastructure.adapters.storage_adapter import StorageAdapterProvider

adapters_providers = (
    AIAdapterProvider(),
    StorageAdapterProvider(),
)
