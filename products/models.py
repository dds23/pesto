from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, CheckConstraint("price >= 0"), nullable=False)
    version = Column(Integer, nullable=False, default=1)
