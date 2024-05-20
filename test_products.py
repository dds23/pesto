import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from products.database import Base, get_db
from products.main import app
from products.models import Product
from auth.models import User
from products.schemas import ProductCreate, ProductUpdate, ProductSort
from auth.security import create_access_token


# Create a test client
client = TestClient(app)

# Helper function to create a test user and get a token
def create_test_user_and_get_token():
    db = get_db()
    user = User(username="testuser", email="testuser@example.com", password_hash="hashedpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return user.id, token

def test_create_product():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}

    product_data = {
        "name": "Test Product",
        "description": "A product for testing",
        "price": 100.0,
        "version": 1
    }

    response = client.post("/", json=product_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_list_products():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a product
    product = Product(name="Specific Product", description="A specific product", price=150.0, version=1)
    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.get(f"/{product.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Specific Product"

def test_update_product():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a product
    product = Product(name="Update Product", description="A product to be updated", price=200.0, version=1)
    db.add(product)
    db.commit()
    db.refresh(product)

    update_data = {
        "name": "Updated Product",
        "description": "Updated product description",
        "price": 250.0,
        "version": 1
    }

    response = client.put(f"/{product.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

def test_delete_product():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a product
    product = Product(name="Delete Product", description="A product to be deleted", price=300.0, version=1)
    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.delete(f"/{product.id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == "Product deleted successfully"
