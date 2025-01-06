from pydantic import BaseModel, ConfigDict, Field


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


# class JWTValidateUser(BaseModel):
#     model_config = ConfigDict(from_attributes=True, strict=True)

#     object_id: PydanticObjectId = Field(
#         ..., description="unique subject identifier (user ID from MongoDB)"
#     )
#     name: str = Field(..., description="user name")
#     email: str = Field(..., description="user email")
#     password: bytes = Field(..., description="user hashed password")


class JWTTokenInfo(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str | None = Field(default=None, description="JWT refresh token")
    token_type: str | None = Field(default="Bearer", description="token type")
