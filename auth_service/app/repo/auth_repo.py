from typing import Type

import bcrypt
from auth_service.app.DB.models.beanie_models import User
from auth_service.app.DB.models.pydantic_models import RegisterUser
from beanie import Document


class AuthRepo:
    def __init__(self, user_model: Type[Document]):
        self._user_model = user_model

    def _hash_password(
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
            password=self._hash_password(user_data.password),
        )
        return await self._user_model.insert_one(user)

    async def fetched_user_data(self, email: str) -> Document:
        find_res = await self._user_model.find_one({"email": email})
        assert find_res is not None
        return find_res
