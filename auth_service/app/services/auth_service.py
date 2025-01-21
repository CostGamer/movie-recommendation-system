from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from auth_service.app.core import all_configs
from auth_service.app.core.config import ACCESS_TOKEN, REFRESH_TOKEN, TOKEN_TYPE_FIELD
from auth_service.app.core.custom_exceptions import (
    InvalidUsernameOrPasswordError,
    TroublesWithRegistrationError,
    UserWithThisEmailExistsError,
)
from auth_service.app.DB.models.beanie_models import User
from auth_service.app.DB.models.pydantic_models import (
    EventType,
    JWTTokenInfo,
    JWTValidateUser,
    RegisterUser,
)
from auth_service.app.repo.auth_repo import AuthRepo
from auth_service.app.services.common_service import EventsService
from email_validator import EmailNotValidError, validate_email


class CommonAuthService:
    def __init__(
        self,
    ) -> None:
        pass

    async def encode_jwt(
        self,
        payload: dict,
        private_key: str = all_configs.jwt.private_key_path.read_text(),
        algorithm: str = all_configs.jwt.algorithm,
        expire_minutes: int = all_configs.jwt.access_jwt_expire_min,
    ) -> str:
        payload_to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=expire_minutes)
        payload_to_encode.update(iat=now, exp=expire)
        encoded_jwt = jwt.encode(
            payload=payload_to_encode,
            key=private_key,
            algorithm=algorithm,
        )
        return encoded_jwt

    async def decode_jwt(
        self,
        token: str | bytes,
        public_key: str = all_configs.jwt.public_key_path.read_text(),
        algorithm: str = all_configs.jwt.algorithm,
    ) -> dict:
        decoded = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=algorithm,
        )
        return decoded

    async def create_jwt(
        self,
        token_type: str,
        token_payload: dict | None = None,
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        if token_payload is not None:
            jwt_payload.update(token_payload)
        return await self.encode_jwt(
            payload=jwt_payload,
        )

    async def create_access_token(self, user_id: str) -> str:
        initial_payload = {"sub": user_id}
        return await self.create_jwt(
            token_type=ACCESS_TOKEN,
            token_payload=initial_payload,
        )

    async def create_refresh_token(self) -> str:
        return await self.create_jwt(
            token_type=REFRESH_TOKEN,
        )

    async def validate_password(
        self,
        password: str,
        hash_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hash_password,
        )


class RegisterUserService:
    def __init__(
        self,
        auth_repo: AuthRepo,
        events_service: EventsService,
    ) -> None:
        self._auth_repo = auth_repo
        self._events_service = events_service

    async def __call__(self, user_data: RegisterUser) -> str | None:
        try:
            self._check_valid_email(user_data.email)
            check_email_already_exists = (
                await self._auth_repo.check_email_already_exists(user_data.email)
            )
            if check_email_already_exists:
                raise UserWithThisEmailExistsError

            res = await self._auth_repo.insert_registered_user_to_db(user_data)
            if res is None:
                raise TroublesWithRegistrationError

            await self._events_service._create_event(
                user_id=str(res.id),
                event_type=EventType.USER_CREATED,
                payload={"email": user_data.email},
            )

            return str(res.id)
        except:
            await self._events_service._create_event(
                event_type=EventType.USER_ISSUE, payload={"email": user_data.email}
            )
            raise

    def _check_valid_email(self, email: str) -> None:
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise e


class LoginUserService:
    def __init__(
        self,
        auth_repo: AuthRepo,
        common_auth_service: CommonAuthService,
        events_service: EventsService,
    ) -> None:
        self._auth_repo = auth_repo
        self._common_auth_service = common_auth_service
        self._events_service = events_service

    async def __call__(self, email: str, password: str) -> JWTTokenInfo | None:
        try:
            validated_user = await self._validate_auth_user(email, password)
            access_token = await self._common_auth_service.create_access_token(
                validated_user.object_id
            )
            refresh_token = await self._common_auth_service.create_refresh_token()

            await self._events_service._create_event(
                event_type=EventType.USER_LOGIN, payload={"email": email}
            )

            return JWTTokenInfo(access_token=access_token, refresh_token=refresh_token)
        except:
            await self._events_service._create_event(
                event_type=EventType.USER_ISSUE, payload={"email": email}
            )
            raise

    async def _validate_auth_user(self, email: str, password: str) -> JWTValidateUser:
        check_email_already_exists = await self._auth_repo.check_email_already_exists(
            email
        )
        if not check_email_already_exists:
            raise InvalidUsernameOrPasswordError

        user_fetched_data_from_db: User = await self._auth_repo.fetched_user_data(email)

        check_password_correctness = await self._common_auth_service.validate_password(
            password, user_fetched_data_from_db.password.encode()
        )
        if not check_password_correctness:
            raise InvalidUsernameOrPasswordError

        return JWTValidateUser(
            object_id=str(user_fetched_data_from_db.id),
            name=user_fetched_data_from_db.name,
            email=user_fetched_data_from_db.email,
        )
