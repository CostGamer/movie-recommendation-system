from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import all_configs
from app.core.logs import init_logger
from app.middleware.logger import LoggerMiddleware

logger = getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    pass


def init_routers(app: FastAPI) -> None:
    pass


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


def setup_app() -> FastAPI:
    app = FastAPI(
        title="Auth Service API",
        description="Provide auth of new users & log in for existing users",
        version="0.1.0",
    )
    init_logger(all_configs.logging)
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
