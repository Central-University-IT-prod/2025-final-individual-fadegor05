from collections.abc import Iterable

from dishka import AsyncContainer, Provider, make_async_container

from src.application.services import services_providers
from src.application.use_cases import use_cases_providers
from src.core.settings import Settings, SettingsProvider, get_settings
from src.infrastructure.adapters import adapters_providers
from src.infrastructure.db.database import AsyncSessionProvider
from src.infrastructure.db.repositories import repositories_providers


def get_providers() -> Iterable[Provider]:
    return (
        SettingsProvider(),
        AsyncSessionProvider(),
        *adapters_providers,
        *repositories_providers,
        *services_providers,
        *use_cases_providers,
    )


def create_async_container(providers: Iterable[Provider]) -> AsyncContainer:
    settings = get_settings()
    return make_async_container(
        *providers,
        context={Settings: settings},
    )
