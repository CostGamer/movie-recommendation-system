from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EventType(str, Enum):
    USER_CREATED = "UserCreated"
    USER_LOGIN = "UserLogin"
    USER_ISSUE = "Problem"


class RegisterUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., description="user email")
    password: str = Field(..., description="user password", min_length=8)
    name: str = Field(..., description="user name")
    age: int = Field(..., description="user age")


class GetUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="user first name")
    age: int = Field(..., description="user's age")
    email: str = Field(..., description="user email")


class JWTValidateUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    object_id: str = Field(
        ..., description="unique subject identifier (user ID from MongoDB)"
    )
    name: str = Field(..., description="user name")
    email: str = Field(..., description="user email")


class JWTTokenInfo(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str | None = Field(default=None, description="JWT refresh token")
    token_type: str | None = Field(default="Bearer", description="token type")


class EventP(BaseModel):
    user_id: str | None = Field(..., description="Unique identifier of the user")
    event_type: EventType = Field(
        ..., description="Type of the event (e.g., UserCreated, UserLogin)"
    )
    payload: dict[str, Any] = Field(
        ..., description="Additional data related to the event"
    )
