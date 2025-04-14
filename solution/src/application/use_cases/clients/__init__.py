from src.application.use_cases.clients.create_clients_use_case import (
    CreateClientsUseCaseProvider,
)
from src.application.use_cases.clients.get_client_use_case import (
    GetClientUseCaseProvider,
)

clients_use_cases_providers = (
    CreateClientsUseCaseProvider(),
    GetClientUseCaseProvider(),
)
