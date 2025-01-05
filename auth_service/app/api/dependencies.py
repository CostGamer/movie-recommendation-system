from auth_service.app.DB.models.beanie_models import User
from auth_service.app.repo.auth_repo import AuthRepo
from auth_service.app.services.auth_service import RegisterUserService
from fastapi import Depends


def get_auth_repo() -> AuthRepo:
    return AuthRepo(user_model=User)


def get_register_user_service(
    auth_repo: AuthRepo = Depends(get_auth_repo),
) -> RegisterUserService:
    return RegisterUserService(auth_repo)
