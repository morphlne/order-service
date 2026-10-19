from sqlalchemy import Column, Integer, String

from config.db import Base    

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email
