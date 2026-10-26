from fastapi import HTTPException

from repositories.user_repository import *
from schemas.user import UserActive

emails = set()


def update_emails(db: Session):
    users = get_all(db)
    for user in users:
        emails.add(user.email)
    print("Emails updated: " + ', '.join(emails))


def get_all_users(db: Session):
    users = get_all(db)
    return [user for user in users if user.is_active]


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


def make_user_inactive(user_id: int, user: UserActive, db: Session):
    if user.is_active:
        raise HTTPException(status_code=400, detail="User activation is not supported")
    user_db = get_user(user_id, db)
    inactive = make_inactive(user_db, db)
    return {"message": "User inactive", "user": inactive}
