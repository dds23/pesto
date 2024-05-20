from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserCreate, UserLogin
from services import register_user, authenticate_user
from database import get_db

router = APIRouter()

@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user_data)

@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return authenticate_user(db, user_data)