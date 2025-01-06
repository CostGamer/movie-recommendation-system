from auth_service.app.core.custom_exceptions import (
    TroublesWithRegistrationError,
    UserWithThisEmailExistsError,
)
from fastapi import Request
from fastapi.responses import JSONResponse


async def email_already_exists_error(
    request: Request, exc: UserWithThisEmailExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "This email already in the system"},
    )


async def registration_troubles_error(
    request: Request, exc: TroublesWithRegistrationError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": "Some problems with insertion to db"},
    )


async def invalid_username_or_password_error(
    request: Request, exc: UserWithThisEmailExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Email or password Not Found"},
    )
