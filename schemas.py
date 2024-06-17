from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ProductCreate(BaseModel):
    name: str
    quantity: int
    price: float

class UpdateQuantity(BaseModel):
    quantity: int

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    total_price: float
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    author_id: int
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    author_id: int

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    comments: List[Comment] = []

    class Config:
        from_attributes = True