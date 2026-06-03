from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class UserCreateSchema(BaseModel):
    username: str | None = Field(
        default=None,
        max_length=64,
    )
    telegram_id: int


class UserResponseSchema(BaseModel):
    id: int
    username: str | None = Field(
        default=None,
        max_length=64,
    )
    telegram_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
