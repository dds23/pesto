from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orders.database import get_db
from orders.main import app  # Import your FastAPI app
from orders.models import Order, OrderItem, Product, User, Base  # Import necessary models
from orders.schemas import OrderCreate, OrderItemCreate, OrderStatus
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

def test_create_order():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a product
    product = Product(id=1, name="Test Product", price=10.0, version=1)
    db.add(product)
    db.commit()

    order_data = {
        "order_items": [
            {"product_id": 1, "quantity": 2}
        ]
    }

    response = client.post("/", json=order_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["total_price"] == 20.0

def test_get_orders():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_order():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a product and an order
    product = Product(id=2, name="Another Product", price=15.0, version=1)
    db.add(product)
    db.commit()

    order = Order(user_id=user_id, total_price=30.0)
    db.add(order)
    db.commit()
    db.refresh(order)

    order_item = OrderItem(order_id=order.id, product_id=2, quantity=2, price=15.0)
    db.add(order_item)
    db.commit()

    response = client.get(f"/{order.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == order.id

def test_update_order_status():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a product and an order
    product = Product(id=3, name="Product for Update", price=20.0, version=1)
    db.add(product)
    db.commit()

    order = Order(user_id=user_id, total_price=40.0, order_status="Pending")
    db.add(order)
    db.commit()
    db.refresh(order)

    order_item = OrderItem(order_id=order.id, product_id=3, quantity=2, price=20.0)
    db.add(order_item)
    db.commit()

    update_data = {"order_status": "Shipped"}

    response = client.put(f"/{order.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["order_status"] == "Shipped"

def test_create_order_with_deleted_product():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a product and mark it as deleted (version = 0)
    product = Product(id=4, name="Deleted Product", price=10.0, version=0)
    db.add(product)
    db.commit()

    order_data = {
        "order_items": [
            {"product_id": 4, "quantity": 1}
        ]
    }

    response = client.post("/", json=order_data, headers=headers)
    assert response.status_code == 404
    assert "Order contains deleted product" in response.json()["detail"]
