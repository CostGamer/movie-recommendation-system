from auth_service.app.DB.models.beanie_models import Event, User
from auth_service.app.repo.auth_repo import AuthRepo
from auth_service.app.repo.events_repo import EventsRepo
from auth_service.app.services.auth_service import (
    CommonAuthService,
    LoginUserService,
    RegisterUserService,
)
from auth_service.app.services.common_service import EventsService
from fastapi import Depends, Request


def get_auth_repo() -> AuthRepo:
    return AuthRepo(user_model=User)


def get_events_repo() -> EventsRepo:
    return EventsRepo(event_model=Event)


def get_common_auth_service() -> CommonAuthService:
    return CommonAuthService()


def get_events_service(
    request: Request, event_repo: EventsRepo = Depends(get_events_repo)
) -> EventsService:
    return EventsService(event_repo=event_repo, request=request)


def get_register_user_service(
    auth_repo: AuthRepo = Depends(get_auth_repo),
    events_service: EventsService = Depends(get_events_service),
) -> RegisterUserService:
    return RegisterUserService(auth_repo, events_service)


def get_login_user_service(
    auth_repo: AuthRepo = Depends(get_auth_repo),
    common_auth_service: CommonAuthService = Depends(get_common_auth_service),
    events_service: EventsService = Depends(get_events_service),
) -> LoginUserService:
    return LoginUserService(auth_repo, common_auth_service, events_service)
