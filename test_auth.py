from fastapi.testclient import TestClient
from auth.main import app

client = TestClient(app)

def test_register_user():
        response = client.post(
            "/api/auth/register", json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"})
        assert response.status_code == 200
        assert response.json() == {"message": "User registered successfully"}


def test_register_user_existing_username():
    client.post("/api/auth/register", json={"username": "testuser2",
                "email": "testuser2@example.com", "password": "testpassword"})
    response = client.post("/api/auth/register", json={"username": "testuser2",
                        "email": "testuser2@example.com", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already taken"}


def test_login_user():
    client.post("/api/auth/register", json={"username": "loginuser",
                "email": "loginuser@example.com", "password": "loginpassword"})
    response = client.post(
        "/api/auth/login", json={"username": "loginuser", "password": "loginpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_user_invalid_username():
    response = client.post(
        "/api/auth/login", json={"username": "invaliduser", "password": "somepassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}


def test_login_user_invalid_password():
    client.post("/api/auth/register", json={"username": "invalidpassuser",
                "email": "invalidpassuser@example.com", "password": "validpassword"})
    response = client.post(
        "/api/auth/login", json={"username": "invalidpassuser", "password": "invalidpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}
