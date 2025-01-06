from auth_service.app.core.custom_exceptions import (
    InvalidUsernameOrPasswordError,
    TroublesWithRegistrationError,
    UserWithThisEmailExistsError,
)
from auth_service.app.DB.models.beanie_models import User
from auth_service.app.DB.models.pydantic_models import (
    JWTTokenInfo,
    JWTValidateUser,
    RegisterUser,
)
from auth_service.app.repo.auth_repo import AuthRepo


class RegisterUserService:
    def __init__(
        self,
        auth_repo: AuthRepo,
    ) -> None:
        self._auth_repo = auth_repo

    async def __call__(self, user_data: RegisterUser) -> str:
        check_email_already_exists = await self._auth_repo.check_email_already_exists(
            user_data.email
        )
        if check_email_already_exists:
            raise UserWithThisEmailExistsError

        res = await self._auth_repo.insert_registered_user_to_db(user_data)
        if res is None:
            raise TroublesWithRegistrationError

        return str(res.id)


class LoginUserService:
    def __init__(
        self,
        auth_repo: AuthRepo,
    ) -> None:
        self._auth_repo = auth_repo

    async def __call__(self, email: str, password: str) -> JWTTokenInfo:
        validated_user = await self.validate_auth_user(email, password)
        access_token = await self._auth_repo.create_access_token(
            validated_user.object_id
        )
        refresh_token = await self._auth_repo.create_refresh_token()
        return JWTTokenInfo(access_token=access_token, refresh_token=refresh_token)

    async def validate_auth_user(self, email: str, password: str) -> JWTValidateUser:
        check_email_already_exists = await self._auth_repo.check_email_already_exists(
            email
        )
        if not check_email_already_exists:
            raise InvalidUsernameOrPasswordError

        user_fetched_data_from_db: User = await self._auth_repo.fetched_user_data(email)

        check_password_correctness = await self._auth_repo.validate_password(
            password, user_fetched_data_from_db.password.encode()
        )
        if not check_password_correctness:
            raise InvalidUsernameOrPasswordError

        return JWTValidateUser(
            object_id=str(user_fetched_data_from_db.id),
            name=user_fetched_data_from_db.name,
            email=user_fetched_data_from_db.email,
        )
