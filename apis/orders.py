from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Order, OrderItem
from schemas import OrderCreate, OrderItemCreate, Order as OrderSchema

router = APIRouter(tags=["orders"])

@router.post("/orders", response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(user_id=order.user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.post("/orders/{id}/items", response_model=OrderSchema)
def add_item_to_order(id: int, item: OrderItemCreate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_item = OrderItem(order_id=id, product_id=item.product_id, quantity=item.quantity, price=item.price)
    db_order.total_price += item.price * item.quantity
    db.add(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/{id}/total", response_model=dict)
def get_order_total(id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": db_order.id, "total_price": db_order.total_price}