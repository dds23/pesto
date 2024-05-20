from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from schemas import TaskStatus

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default=TaskStatus.InDraft)
    version = Column(Integer, nullable=False, default=1)
