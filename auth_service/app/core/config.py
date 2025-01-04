from os import environ as env
from pathlib import Path

from pydantic import BaseModel, Field


class LoggingSettings(BaseModel):
    log_level: str = Field(default="DEBUG", alias="LOG_LEVEL")
    log_file: str = Field(alias="LOG_FILE")
    log_encoding: str = Field(default="utf-8", alias="LOG_ENCODING")


class MongoDatabaseSettings(BaseModel):
    mongo_host: str = Field(default="localhost", alias="MONGO_HOST")
    mongo_port: int = Field(default="0000", alias="MONGO_PORT")
    mongo_db_name: str = Field(default="db", alias="MONGO_DB_NAME")

    @property
    def mongo_db_uri(self) -> str:
        return f"mongodb://{self.mongo_host}:{self.mongo_port}"


class OtherSettings(BaseModel):
    origins: str = Field(
        default="http://localhost:8000,http://127.0.0.1:8000", alias="ALLOWED_IPS"
    )

    @property
    def list_of_origins(self) -> list[str]:
        return self.origins.split(",")


class Settings(BaseModel):
    logging: LoggingSettings = Field(default_factory=lambda: LoggingSettings(**env))
    mongo: MongoDatabaseSettings = Field(
        default_factory=lambda: MongoDatabaseSettings(**env)
    )
    different: OtherSettings = Field(default_factory=lambda: OtherSettings(**env))


def load_dotenv(path: str | Path) -> None:
    path = Path(path)
    if not path.exists():
        return
    with path.open(mode="r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#") or line.strip() == "":
                continue
            key, value = line.strip().split("=", maxsplit=1)
            env.setdefault(key, value)


load_dotenv(".env")
