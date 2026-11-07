from fastapi import HTTPException

from repositories.user_repository import *
from schemas.user import UserActive
from services import email_cache_service as cache


def get_all_users(db: Session):
    users = get_all(db)
    return [user for user in users if user.is_active]


def get_user(user_id: int, db: Session):
    user = get_by_id(user_id, db)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(user: UserBase, db: Session):
    if cache.contains(user.email):
        raise HTTPException(status_code=400, detail="User with email already exists " + user.email)
    saved = save_user(user, db)
    cache.add(saved.email)
    return {"message": "User created", "user": saved}


def update_user(user_id: int, updated_user: UserBase, db: Session):
    user_db = get_user(user_id, db)
    if user_db.email is not updated_user.email:
        if cache.contains(updated_user.email):
            raise HTTPException(status_code=400, detail="User with email already exists " + updated_user.email)
        old_email = user_db.email
        update(user_db, updated_user, db)
        cache.change(old_email, user_db.email)
    else:
        update(user_db, updated_user, db)
    return {"message": "User updated", "user": user_db}


def make_user_inactive(user_id: int, user: UserActive, db: Session):
    if user.is_active:
        raise HTTPException(status_code=400, detail="User activation is not supported")
    user_db = get_user(user_id, db)
    inactive = make_inactive(user_db, db)
    return {"message": "User inactive", "user": inactive}
