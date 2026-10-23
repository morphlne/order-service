from typing import Annotated

from pydantic import BaseModel, StringConstraints


class UserBase(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    email: Annotated[str, StringConstraints(strip_whitespace=True, min_length=6)]


class UserActive(BaseModel):
    is_active: bool
