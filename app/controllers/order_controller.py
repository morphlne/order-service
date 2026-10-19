from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.order import OrderBase
from config.db import get_db
import services.order_service as orders

router = APIRouter()

@router.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    return orders.get_all_orders(db)

@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    return orders.get_order(order_id, db)

@router.post("/orders")
def create_order(order: OrderBase, db: Session = Depends(get_db)):
    return orders.create_order(order, db)

@router.put("/orders/{order_id}")
def update_order(order_id: int, updated_order: OrderBase, db: Session = Depends(get_db)):
    return orders.update_order(order_id, updated_order, db)

@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return orders.delete_order(order_id, db)
