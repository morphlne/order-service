from datetime import date

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    date: date
    payment: int
