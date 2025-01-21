from auth_service.app.api.dependencies import (
    get_login_user_service,
    get_register_user_service,
)
from auth_service.app.api.responses import login_user_responses, register_user_responses
from auth_service.app.DB.models.pydantic_models import JWTTokenInfo, RegisterUser
from auth_service.app.services.auth_service import LoginUserService, RegisterUserService
from fastapi import APIRouter, Depends

auth_router = APIRouter()


@auth_router.post(
    "/register_user",
    response_model=str,
    responses=register_user_responses,
    description="endpoint for register user",
)
async def register_user(
    user_data: RegisterUser,
    register_user_service: RegisterUserService = Depends(get_register_user_service),
) -> str:
    return await register_user_service(user_data)


@auth_router.post(
    "/login_user",
    response_model=JWTTokenInfo,
    responses=login_user_responses,
    description="endpoint for login user",
)
async def login_user(
    email: str,
    password: str,
    login_user_service: LoginUserService = Depends(get_login_user_service),
) -> JWTTokenInfo:
    return await login_user_service(email, password)
