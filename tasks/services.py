from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskSort, TaskFilter


# Function to add a new task
def create_task(db: Session, task_data: TaskCreate):
    new_task = Task(**task_data.model_dump())
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except:
        raise HTTPException(status_code=400, detail='Could not add task')


# Fetch all tasks
def get_tasks(db: Session, sort_by: TaskSort, filter_by: TaskFilter):
    '''
        This will sort the task results based on name in ascending or
        descending manner based on the input provided.
    '''
    query = db.query(Task).filter(Task.version != 0)

    if filter_by != TaskFilter.All:
        query = query.filter_by(Task.status == filter_by)

    if sort_by == TaskSort.Title_A_to_Z:
        query = query.order_by(Task.title.asc())
    elif sort_by == TaskSort.Title_Z_to_A:
        query = query.order_by(Task.title.desc())
    elif sort_by == TaskSort.Status_A_to_Z:
        query = query.order_by(Task.status.asc())
    else:
        query = query.order_by(Task.status.desc())

    return query.all()


# Fetch a specific task
def get_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.version != 0).one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update the information of a specific task
def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = db.query(Task).filter(
        Task.id == task_id, Task.version != 0).with_for_update().one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.version != task_data.version:
        raise HTTPException(
            status_code=409, detail="Task has been modified by another user")

    task.title = task_data.title
    task.status = task_data.status
    task.description = task_data.description
    task.version += 1

    db.commit()
    db.refresh(task)
    return task


# Function to delete a specific task
def delete_task(db: Session, task_id: int):
    '''
        This function is for deleting a specific task but does not literally
        delete the task from the database.

        If we actually delete a task, the order information will get affected but it is something
        which has to be stored for eternity. For this purpose a task is marked as deleted when its
        version is set to 0. From here on out, only tasks other than version = 0 will be treated as
        live tasks. 
    '''
    task = db.query(Task).filter(Task.id == task_id, Task.version != 0).one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.version = 0
    db.commit()
    return 'Task deleted successfully'
