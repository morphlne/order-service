from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import services.user_service as users
from config.db import get_db
from schemas.user import UserBase, UserActive, UserResponse, UserWrapper

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return users.get_all_users(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return users.get_user(user_id, db)


@router.post("/users", response_model=UserWrapper)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    return users.create_user(user, db)


@router.put("/users/{user_id}", response_model=UserWrapper)
def update_user(user_id: int, updated_user: UserBase, db: Session = Depends(get_db)):
    return users.update_user(user_id, updated_user, db)


@router.patch("/users/{user_id}", response_model=UserWrapper)
def make_user_inactive(user_id: int, user: UserActive, db: Session = Depends(get_db)):
    return users.make_user_inactive(user_id, user, db)
