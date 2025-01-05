from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncGenerator

from auth_service.app.api.auth_routes import auth_router
from auth_service.app.api.exceptions import (
    email_already_exists_error,
    registration_troubles_error,
)
from auth_service.app.core import all_configs
from auth_service.app.core.custom_exceptions import (
    TroublesWithRegistrationError,
    UserWithThisEmailExistsError,
)
from auth_service.app.core.logs import init_logger
from auth_service.app.DB import mongo_db_init
from auth_service.app.middleware.logger import LoggerMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserWithThisEmailExistsError, email_already_exists_error)  # type: ignore
    app.add_exception_handler(
        TroublesWithRegistrationError, registration_troubles_error  # type: ignore
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(auth_router)


def init_middlewares(app: FastAPI) -> None:
    origins = all_configs.different.list_of_origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggerMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await mongo_db_init.init()
    yield
    await mongo_db_init.close()


def setup_app() -> FastAPI:
    app = FastAPI(
        title="Auth Service API",
        description="Provide auth of new users & log in for existing users",
        version="0.1.0",
        lifespan=lifespan,
    )
    init_logger(all_configs.logging)
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
