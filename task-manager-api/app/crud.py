from sqlmodel import Session, select
from typing import List, Optional, Sequence
from datetime import datetime
from sqlmodel import or_
from app.model import Task, TaskStatus, TaskPriority
from app.schemas import TaskCreate, TaskUpdate


# ✅ Create a new task
def create_task(session: Session, task_data: TaskCreate) -> Task:
    task = Task.from_orm(task_data)
    task.created_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# ✅ Get all tasks (optionally filter by status or priority)
def get_filtered_tasks(
    session: Session,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    q: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "asc"
) -> List[Task]:
    statement = select(Task)

    # Filters
    if status:
        statement = statement.where(Task.status == status)
    if priority:
        statement = statement.where(Task.priority == priority)
    if q:
        search = f"%{q.lower()}%"
        statement = statement.where(
            or_(
                Task.title.ilike(search),
                Task.description.ilike(search)
            )
        )

    # Sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    statement = statement.order_by(sort_column)
    return session.exec(statement).all()


# ✅ Get task by ID
def get_task_by_id(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)


# ✅ Update a task
def update_task(session: Session, task: Task, updates: TaskUpdate) -> Task:
    task_data = updates.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# ✅ Delete a task
def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.commit()


def get_tasks_by_status(session: Session, status: TaskStatus) -> List[Task]:
    statement = select(Task).where(Task.status == status)
    return session.exec(statement).all()

def get_tasks_by_priority(session: Session, priority: TaskPriority) -> List[Task]:
    statement = select(Task).where(Task.priority == priority)
    return session.exec(statement).all()