from sqlalchemy.orm import Session

from models.order import Order
from schemas.order import OrderBase

def get_all(db: Session):
    return db.query(Order).all()

def get_by_id(order_id: int, db: Session):
    return db.query(Order).filter(Order.order_id == order_id).first()

def save_order(order: OrderBase, db: Session):
    order_db = Order(order.user_id, order.date, order.payment)
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db

def update(order_db: Order, order: OrderBase, db: Session):
    order_db.user_id = order.user_id
    order_db.date = order.date
    order_db.payment = order.payment
    db.commit()
    db.refresh(order_db)
    return order_db

def delete(order: Order, db: Session):
    db.delete(order)
    db.commit()
    return order
