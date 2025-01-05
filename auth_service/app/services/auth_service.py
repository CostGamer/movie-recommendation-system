from auth_service.app.core.custom_exceptions import (
    TroublesWithRegistrationError,
    UserWithThisEmailExistsError,
)
from auth_service.app.DB.models.pydantic_models import RegisterUser
from auth_service.app.repo.auth_repo import AuthRepo


class RegisterUserService:
    def __init__(
        self,
        auth_repo: AuthRepo,
    ) -> None:
        self._auth_repo = auth_repo

    async def __call__(self, user_data: RegisterUser) -> str:
        check_email_already_exists = await self._auth_repo.check_email_already_exists(
            user_data
        )
        if check_email_already_exists:
            raise UserWithThisEmailExistsError

        res = await self._auth_repo.insert_registered_user_to_db(user_data)
        if res is None:
            raise TroublesWithRegistrationError

        return str(res.id)
