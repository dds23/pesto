from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin
from security import get_password_hash, verify_password, create_access_token


def register_user(db: Session, user_data: UserCreate):
    # Check if user already exists
    existing_user = db.query(User).filter(
        User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password
    password_hash = get_password_hash(user_data.password)

    # Create a new user
    new_user = User(username=user_data.username,
                    email=user_data.email, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


def authenticate_user(db: Session, user_data: UserLogin):
    # Find the user
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    # Verify the password
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    # Generate and return a JWT token
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
