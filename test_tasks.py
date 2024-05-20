import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tasks.database import Base, get_db
from tasks.main import app
from tasks.models import Task
from auth.models import User
from tasks.schemas import TaskCreate, TaskUpdate, TaskSort
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

def test_create_task():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}

    task_data = {
        "title": "Test Task",
        "description": "A task for testing",
        "status": "pending",
        "version": 1
    }

    response = client.post("/", json=task_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_list_tasks():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a task
    task = Task(title="Specific Task", description="A specific task", status="pending", version=1)
    db.add(task)
    db.commit()
    db.refresh(task)

    response = client.get(f"/{task.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Task"

def test_update_task():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a task
    task = Task(title="Update Task", description="A task to be updated", status="pending", version=1)
    db.add(task)
    db.commit()
    db.refresh(task)

    update_data = {
        "title": "Updated Task",
        "description": "Updated task description",
        "status": "completed",
        "version": 1
    }

    response = client.put(f"/{task.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

def test_delete_task():
    user_id, token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    db = get_db()

    # Add a task
    task = Task(title="Delete Task", description="A task to be deleted", status="pending", version=1)
    db.add(task)
    db.commit()
    db.refresh(task)

    response = client.delete(f"/{task.id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == "Task deleted successfully"
