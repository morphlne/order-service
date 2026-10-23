from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base
from models.order import Order


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    orders: Mapped[list[Order]] = relationship()

    def __init__(self, name, email):
        self.name = name
        self.email = email
