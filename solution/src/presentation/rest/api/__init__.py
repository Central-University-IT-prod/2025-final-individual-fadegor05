from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.rest.api.ads import router as ads_router
from src.presentation.rest.api.advertisers import router as advertisers_router
from src.presentation.rest.api.banwords import router as banwords_router
from src.presentation.rest.api.campaigns import router as campaigns_router
from src.presentation.rest.api.cdn import router as cdn_router
from src.presentation.rest.api.clients import router as clients_router
from src.presentation.rest.api.generate import router as generate_router
from src.presentation.rest.api.stats import router as stats_router
from src.presentation.rest.api.time import router as time_router

subrouters = (
    clients_router,
    advertisers_router,
    campaigns_router,
    ads_router,
    stats_router,
    time_router,
    generate_router,
    cdn_router,
    banwords_router,
)

api_router = APIRouter(prefix="", route_class=DishkaRoute)

for subrouter in subrouters:
    api_router.include_router(subrouter)
