from typing import Optional
from datetime import datetime , timezone
from sqlmodel import SQLModel
from app.model import TaskPriority, TaskStatus
from pydantic import validator


# ✅ Schema for creating a task (POST /tasks)
class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.pending
    priority: Optional[TaskPriority] = TaskPriority.medium
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

    @validator("title")
    def validate_title(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty or whitespace only")
        return v

    @validator("due_date")
    def validate_due_date(cls, v):
        if v is not None and v <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return v


# ✅ Schema for updating a task (PUT /tasks/{id})
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

    @validator("title")
    def validate_title(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty or whitespace only")
        return v

    @validator("due_date")
    def validate_due_date(cls, v):
        if v is not None and v <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return v


# ✅ Schema for reading a task (GET /tasks or GET /tasks/{id})
class TaskRead(SQLModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

    class Config:
        orm_mode = True
