import uvicorn
from dishka.integrations.fastapi import (
    setup_dishka,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.core.providers import create_async_container, get_providers
from src.core.settings import get_settings
from src.presentation.rest.api import api_router
from src.presentation.rest.exceptions import (
    DetailedHTTPException,
    detailed_http_exception_handler,
    validation_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(title="HypeAgency API")
    app.include_router(api_router)
    app.add_exception_handler(DetailedHTTPException, detailed_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    providers = get_providers()
    container = create_async_container(providers)
    setup_dishka(container=container, app=app)
    return app


def startup_rest() -> None:
    app = create_app()
    uvicorn.run(app, host="REDACTED", port=get_settings().server.port)


if __name__ == "__main__":
    startup_rest()
