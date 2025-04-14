from enum import Enum

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.presentation.rest.schemas.common_schema import IDetailedException


def detailed_http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=IDetailedException(message=exc.detail).model_dump(),
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=IDetailedException(message="Ошибка в данных запроса.").model_dump(),
    )


class ExceptionEnum(Enum):
    VALIDATION_ERROR = ("Ошибка валидации", 400)
    NO_AUTH = ("Не авторизован", 401)
    NO_ACCESS = ("Нет доступа", 403)
    NOT_FOUND = ("Не найден", 404)
    ALREADY_EXISTS = ("Конфликт", 409)

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


class DetailedHTTPException(HTTPException):
    def __init__(self, exception_enum: ExceptionEnum):
        super().__init__(
            status_code=exception_enum.status_code, detail=exception_enum.message
        )
