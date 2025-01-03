from datetime import datetime as dt
from datetime import timezone
from typing import Any

from beanie import Document
from pydantic import Field


class User(Document):
    email: str = Field(..., description="user email")
    password: str = Field(..., description="user hashed password")
    name: str = Field(..., description="user name")
    age: int = Field(..., description="user age")

    class Settings:
        name = "users"


class Event(Document):
    aggregate_id: str = Field(..., description="some ID")
    event_type: str = Field(
        ..., description="type of event ex: UserCreated, UserUpdated, etc"
    )
    payload: dict[str, Any] = Field(..., description="all necessary info from query")
    created_at: dt = dt.now(timezone.utc)

    class Settings:
        name = "events"
