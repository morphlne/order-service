from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserBase
from repositories.user_repository import *

emails = set()

def get_all_users(db: Session):
    return get_all(db)

def get_user(user_id: int, db: Session):
    user = get_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user(user: UserBase, db: Session):
    if user.email in emails:
        raise HTTPException(status_code=400, detail="User with email already exists " + user.email)
    emails.add(user.email)
    saved = save_user(user, db)
    return {"message": "User created", "user": saved}

def update_user(user_id: int, updated_user: UserBase, db: Session):
    user_db = get_user(user_id, db)
    emails.discard(user_db.email)
    if updated_user.email in emails:
        emails.add(user_db.email)
        raise HTTPException(status_code=400, detail="User with email already exists " + updated_user.email)
    update(user_db, updated_user, db)
    emails.add(updated_user.email)
    return {"message": "User updated", "user": updated_user}

def delete_user(user_id: int, db: Session):
    user_db = get_user(user_id, db)
    deleted = delete(user_db, db)
    emails.discard(user_db.email)
    return {"message": "User deleted", "user": deleted}
