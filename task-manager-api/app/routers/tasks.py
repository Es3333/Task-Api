from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from sqlmodel import Session

from app.database import get_session
from app.schemas import TaskCreate, TaskRead, TaskUpdate
from app.model import TaskStatus, TaskPriority
from app import crud

router = APIRouter()


# ✅ Create a new task
@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create(task: TaskCreate, session: Session = Depends(get_session)):
    return crud.create_task(session, task)


# ✅ Get all tasks
@router.get("/", response_model=List[TaskRead])
def read_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    q: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "asc",
    session: Session = Depends(get_session)
):
    return crud.get_filtered_tasks(
        session=session,
        status=status,
        priority=priority,
        q=q,
        sort_by=sort_by,
        sort_order=sort_order
    )


# ✅ Get a single task by ID
@router.get("/{task_id}", response_model=TaskRead)
def read_one(task_id: int, session: Session = Depends(get_session)):
    task = crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# ✅ Update a task
@router.put("/{task_id}", response_model=TaskRead)
def update(task_id: int, updates: TaskUpdate, session: Session = Depends(get_session)):
    task = crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(session, task, updates)


# ✅ Delete a task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(task_id: int, session: Session = Depends(get_session)):
    task = crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(session, task)
@router.get("/status/{status}", response_model=List[TaskRead])
def filter_by_status(status: TaskStatus, session: Session = Depends(get_session)):
    return crud.get_tasks_by_status(session, status)


@router.get("/priority/{priority}", response_model=List[TaskRead])
def filter_by_priority(priority: TaskPriority, session: Session = Depends(get_session)):
    return crud.get_tasks_by_priority(session, priority)