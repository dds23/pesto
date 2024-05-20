from sqlalchemy import Column, Integer, Float, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from schemas import OrderStatus

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, CheckConstraint("price >= 0"), nullable=False)
    version = Column(Integer, nullable=False, default=1)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    total_price = Column(Float, nullable=False)
    order_status = Column(String, nullable=False, default=OrderStatus.Confirmed)
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order = relationship("Order", back_populates="order_items")
