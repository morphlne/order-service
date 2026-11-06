from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict


class UserBase(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    email: EmailStr


class UserActive(BaseModel):
    is_active: bool


class UserResponse(UserBase):
    user_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserWrapper(BaseModel):
    message: str
    user: UserResponse
