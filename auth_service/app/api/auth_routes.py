from auth_service.app.api.dependencies import get_register_user_service
from auth_service.app.api.responses import register_user_responses
from auth_service.app.DB.models.pydantic_models import RegisterUser
from auth_service.app.services.auth_service import RegisterUserService
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
