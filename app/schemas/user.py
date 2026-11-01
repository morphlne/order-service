from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints


class UserBase(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    email: EmailStr


class UserActive(BaseModel):
    is_active: bool
