from datetime import datetime, timedelta, timezone
from typing import Type

import bcrypt
import jwt
from auth_service.app.core import all_configs
from auth_service.app.core.config import ACCESS_TOKEN, REFRESH_TOKEN, TOKEN_TYPE_FIELD
from auth_service.app.DB.models.beanie_models import User
from auth_service.app.DB.models.pydantic_models import RegisterUser
from beanie import Document


class AuthRepo:
    def __init__(self, user_model: Type[Document]):
        self._user_model = user_model

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

    def hash_password(
        self,
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes: bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    async def check_email_already_exists(
        self,
        email: str,
    ) -> bool:
        query = await self._user_model.find_one({"email": email})
        return query is not None

    async def insert_registered_user_to_db(
        self, user_data: RegisterUser
    ) -> Document | None:
        user = User(
            email=user_data.email,
            name=user_data.name,
            age=user_data.age,
            password=self.hash_password(user_data.password),
        )
        return await self._user_model.insert_one(user)

    async def fetched_user_data(self, email: str) -> Document:
        find_res = await self._user_model.find_one({"email": email})
        assert find_res is not None
        return find_res

    async def validate_password(
        self,
        password: str,
        hash_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hash_password,
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
