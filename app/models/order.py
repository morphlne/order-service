from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from config.db import Base


class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    date = Column(Date)
    payment = Column(Integer)

    def __init__(self, user_id, date, payment):
        self.user_id = user_id
        self.date = date
        self.payment = payment
