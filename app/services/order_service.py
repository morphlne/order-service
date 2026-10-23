from fastapi import HTTPException

from repositories.order_repository import *
from services.user_service import get_user


def get_all_orders(db: Session):
    return get_all(db)


def get_order(order_id: int, db: Session):
    order = get_by_id(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def create_order(order: OrderBase, db: Session):
    get_user(order.user_id, db)
    saved = save_order(order, db)
    return {"message": "Order created", "order": saved}


def update_order(order_id: int, updated_order: OrderBase, db: Session):
    order_db = get_order(order_id, db)
    if order_db.user_id != updated_order.user_id:
        get_user(updated_order.user_id, db)
    update(order_db, updated_order, db)
    return {"message": "Order updated", "order": updated_order}


def delete_order(order_id: int, db: Session):
    order_db = get_order(order_id, db)
    deleted = delete(order_db, db)
    return {"message": "Order deleted", "order": deleted}
