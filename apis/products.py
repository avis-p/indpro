from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import SessionLocal, engine, init_db, Product
from schemas import *
from database import get_db

router = APIRouter(tags=["products"])

# init_db()


@router.post("/products")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(name=product.name, quantity=product.quantity, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message": "Product added successfully", "product": db_product}

@router.put("/products/{id}")
def update_quantity(id: int, update: UpdateQuantity, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.quantity = update.quantity
    db.commit()
    return {"message": "Product quantity updated successfully", "product": db_product}

@router.get("/inventory/value")
def get_inventory_value(db: Session = Depends(get_db)):
    total_value = db.query(Product).with_entities(Product.quantity * Product.price).all()
    total_value_sum = sum(value[0] for value in total_value)
    return {"total_value": total_value_sum}