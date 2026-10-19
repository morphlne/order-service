from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user import UserBase
from config.db import get_db
import services.user_service as users

router = APIRouter()

@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return users.get_all_users(db)

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return users.get_user(user_id, db)

@router.post("/users")
def create_user(user: UserBase, db: Session = Depends(get_db)):
    return users.create_user(user, db)

@router.put("/users/{user_id}")
def update_user(user_id: int, updated_user: UserBase, db: Session = Depends(get_db)):
    return users.update_user(user_id, updated_user, db)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return users.delete_user(user_id, db)
