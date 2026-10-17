from fastapi import HTTPException

from models.user import User

users = {}
user_index = 0
emails = set()

def get_all_users():
    return users

def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

def create_user(user: User):
    if user.email in emails:
        raise HTTPException(status_code=400, detail="User with email already exists " + user.email)
    global user_index
    user_index += 1
    users[user_index] = user
    emails.add(user.email)
    return {"message": "User created", "id": user_index, "user": user}

def update_user(user_id: int, updated_user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user = users[user_id]
    emails.remove(user.email)
    if updated_user.email in emails:
        emails.add(user.email)
        raise HTTPException(status_code=400, detail="User with email already exists " + updated_user.email)
    users[user_id] = updated_user
    emails.add(updated_user.email)
    return {"message": "User updated", "user": updated_user}

def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"message": "User deleted"}
