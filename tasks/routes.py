from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import TaskCreate, TaskUpdate, Task, TaskSort, TaskFilter
from services import create_task, get_tasks, get_task, update_task, delete_task
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


# To create a task
@router.post("/", response_model=Task)
async def create(task_data: TaskCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return create_task(db, task_data)


# Fetches all tasks stored in the system
@router.get("/", response_model=list[Task])
async def list_tasks(filter_by: TaskFilter, sort_by: TaskSort, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_tasks(db, sort_by, filter_by)


# Fetch a specific task
@router.get("/{task_id}", response_model=Task)
def get(task_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_task(db, task_id)


# Update a specific task
@router.put("/{task_id}", response_model=Task)
async def update(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return update_task(db, task_id, task_data)


# To delete a specific task
@router.delete("/{task_id}")
async def delete(task_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return delete_task(db, task_id)
