from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import OrderCreate, Order, OrderStatus, OrderFilter, OrderSort
from services import create_order, get_orders, get_order, update_order_status
from database import get_db
from security import verify_token
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from typing import List


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# auth_header = APIKeyHeader(name="token")


# To get user currently logged into the service
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")
    return user_id


# Creates an order for a user
@router.post("/", response_model=Order)
async def create(order_data: OrderCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_order(db, user_id, order_data)


# Fetches all orders for a user
@router.get("/", response_model=List[Order])
async def list_orders(filter_by: OrderFilter, sort_by: OrderSort, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_orders(db, user_id, filter_by, sort_by)


# Fetch a specific order for a user
@router.get("/{order_id}", response_model=Order)
async def get(order_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_order(db, order_id, user_id)


# To update a specific order
@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, order_status: OrderStatus, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_order_status(db, order_id, user_id, order_status)
