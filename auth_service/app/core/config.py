from os import environ as env
from pathlib import Path

from pydantic import BaseModel, Field

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"


class LoggingSettings(BaseModel):
    log_level: str = Field(default="DEBUG", alias="LOG_LEVEL")
    log_file: str = Field(alias="LOG_FILE")
    log_encoding: str = Field(default="utf-8", alias="LOG_ENCODING")


class MongoDatabaseSettings(BaseModel):
    mongo_host: str = Field(default="localhost", alias="MONGO_HOST")
    mongo_port: int = Field(default=0000, alias="MONGO_PORT")
    mongo_db_name: str = Field(default="db", alias="MONGO_DB_NAME")

    @property
    def mongo_db_uri(self) -> str:
        return f"mongodb://{self.mongo_host}:{self.mongo_port}"


class JWTSettings(BaseModel):
    private_key_path: Path = Field(alias="PRIVATE_KEY_PATH")
    public_key_path: Path = Field(alias="PUBLIC_KEY_PATH")
    algorithm: str = Field(default="RS256", alias="JWT_ALGORITHM")
    access_jwt_expire_min: int = Field(default=15, alias="JWT_EXPIRATION_MINUTES")
    refresh_jwt_expire_days: int = Field(default=15, alias="JWT_EXPIRATION_DAYS")


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
    jwt: JWTSettings = Field(default_factory=lambda: JWTSettings(**env))


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
