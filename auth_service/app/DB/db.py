from typing import AsyncIterator, Callable

from auth_service.app.core.config import MongoDatabaseSettings
from auth_service.app.DB.models.beanie_models import Event, User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoDB:
    def __init__(self, mongo_db_settings: MongoDatabaseSettings):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            mongo_db_settings.mongo_db_uri
        )
        self.db: AsyncIOMotorDatabase = self.client[mongo_db_settings.mongo_db_name]

    async def init(self):
        """Инициализация Beanie."""
        await init_beanie(database=self.db, document_models=[User, Event])

    async def close(self):
        """Закрытие клиента."""
        self.client.close()


def get_mongo_client(
    mongo_db: MongoDB,
) -> Callable[[], AsyncIterator[AsyncIOMotorDatabase]]:
    """Генератор для предоставления базы данных."""

    async def receive_db() -> AsyncIterator[AsyncIOMotorDatabase]:
        try:
            yield mongo_db.db
        finally:
            await mongo_db.close()

    return receive_db
