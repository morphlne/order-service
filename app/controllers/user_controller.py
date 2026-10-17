from fastapi import APIRouter

from models.user import User
import services.user_service as users

router = APIRouter()

@router.get("/users")
def get_all_users():
    return users.get_all_users()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    return users.get_user(user_id)

@router.post("/users")
def create_user(user: User):
    return users.create_user(user)

@router.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    return users.update_user(user_id, updated_user)

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return users.delete_user(user_id)
