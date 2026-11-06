from datetime import date

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    user_id: int
    date: date
    payment: int


class OrderResponse(OrderBase):
    order_id: int

    model_config = ConfigDict(from_attributes=True)


class OrderWrapper(BaseModel):
    message: str
    order: OrderResponse
