from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserBase

def get_all(db: Session):
    return db.query(User).all()

def get_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.user_id == user_id).first()

def save_user(user: UserBase, db: Session):
    user_db = User(user.name, user.email)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def update(user_db: User, user: UserBase, db: Session):
    user_db.name = user.name
    user_db.email = user.email
    db.commit()
    db.refresh(user_db)
    return user_db

def delete(user: User, db: Session):
    db.delete(user)
    db.commit()
    return user
