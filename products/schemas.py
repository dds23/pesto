from pydantic import BaseModel, model_validator
from enum import Enum


class ProductBase(BaseModel):
    name: str
    description: str
    price: float

    @model_validator(mode='before')
    def validate_price(cls, value, field):
        if type(value) == dict:
            name = ' '.join(value.get('name').split())
            desc = ' '.join(value.get('description').split())

            if len(name) < 3:
                raise ValueError('Product name has to be a minimum of 3 characters')
            
            if len(desc) < 5:
                raise ValueError('Product description has to be minimum of 5 characters')
            elif not all(char.isalpha() or char.isspace() for char in desc):
                raise ValueError('Description cannot contain any special symbols')
            
            price = value.get('price')
            
            if type(price) not in [float, int]:
                raise ValueError('Price must only be a number')
            if price is not None and price < 0:
                raise ValueError('Price must be non-negative')
            
        return value

    class Config:
        json_encoders = {}


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    version: int


class Product(ProductBase):
    id: int
    version: int

    class Config:
        from_attributes = True


class ProductSort(str, Enum):
    Name_A_to_Z = 'Name_A_to_Z'
    Name_Z_to_A = 'Name_Z_to_A'
    Price_Low_to_High = 'Price_Low_to_High'
    Price_High_to_Low = 'Price_High_to_Low'
