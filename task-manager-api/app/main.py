from fastapi import FastAPI
from app.routers import tasks
from app.database import init_db

app = FastAPI(title="Task Manager API")
init_db()
@app.get("/")
def read_root():
    print("✅ / route hit — new version")
    return {
        "api_name": "Task Manager API",
        "version": "1.0",
        "endpoints": {
            "/": "API information",
            "/health": "Health check",
            "/tasks": "List, create, update, delete tasks",
            "/tasks/{id}": "Get, update or delete task by ID",
            "/tasks/status/{status}": "Filter tasks by status",
            "/tasks/priority/{priority}": "Filter tasks by priority"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])