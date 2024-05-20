from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ProductCreate, ProductUpdate, Product, ProductSort
from services import create_product, get_products, get_product, update_product, delete_product
from database import get_db
from security import verify_token
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# auth_header = APIKeyHeader(name="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")
    return user_id


# To create a product
@router.post("/", response_model=Product)
async def create(product_data: ProductCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return create_product(db, product_data)


# Fetches all products stored in the system
@router.get("/", response_model=list[Product])
async def list_products(sort_by: ProductSort, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_products(db, sort_by)


# Fetch a specific product
@router.get("/{product_id}", response_model=Product)
def get(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_product(db, product_id)


# Update a specific product
@router.put("/{product_id}", response_model=Product)
async def update(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return update_product(db, product_id, product_data)


# To delete a specific product
@router.delete("/{product_id}")
async def delete(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return delete_product(db, product_id)
