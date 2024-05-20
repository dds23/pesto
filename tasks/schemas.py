from pydantic import BaseModel, model_validator
from enum import Enum


class TaskStatus(str, Enum):
    InDraft = 'InDraft'
    Created = 'Created'
    OnHold = 'OnHold'
    InProgress = 'InProgress'
    Completed = 'Completed'


class TaskBase(BaseModel):
    title: str
    description: str
    status: str

    @model_validator(mode='before')
    def validate_task(cls, value, field):
        if type(value) == dict:
            title = ' '.join(value.get('name').split())
            desc = ' '.join(value.get('description').split())

            if len(title) < 3:
                raise ValueError('Task name has to be a minimum of 3 characters')
            
            if len(desc) < 5:
                raise ValueError('Task description has to be minimum of 5 characters')
            elif not all(char.isalpha() or char.isspace() for char in desc):
                raise ValueError('Description cannot contain any special symbols')
            
        return value

    class Config:
        json_encoders = {}


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    version: int
    status: TaskStatus


class Task(TaskBase):
    id: int
    version: int

    class Config:
        from_attributes = True


class TaskSort(str, Enum):
    Title_A_to_Z = 'Title_A_to_Z'
    Title_Z_to_A = 'Title_Z_to_A'
