from pydantic import BaseModel, model_validator
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    Confirmed = 'Confirmed'
    Processed = 'Processed'
    Transit = 'Transit'
    OutForDelivery = 'OutForDelivery'
    Delivered = 'Delivered'


class OrderFilter(str, Enum):
    All = 'All'
    Confirmed = 'Confirmed'
    Processed = 'Processed'
    Transit = 'Transit'
    OutForDelivery = 'OutForDelivery'
    Delivered = 'Delivered'


class OrderSort(str, Enum):
    TotalPrice = 'TotalPrice'
    OrderStatus = 'OrderStatus'


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    price: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    order_items: List[OrderItemCreate]


class OrderCreate(OrderBase):
    @model_validator(mode='before')
    def validate_order_items(cls, values):
        order_items = values.get('order_items', [])
        if not order_items:
            raise ValueError("At least one order item is required")
        return values

    class Config:
        json_encoders = {}


class Order(OrderBase):
    id: int
    user_id: int
    total_price: float
    order_status: OrderStatus
    order_items: List[OrderItem] = []

    class Config:
        from_attributes = True
