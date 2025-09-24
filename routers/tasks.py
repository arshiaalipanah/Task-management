from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from services import task_service, auth_service, project_service
from utils.email import send_email

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.Task)
async def create_task(
    project_id: int,
    task: schemas.TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    # Check project exists
    db_project = project_service.get_project(db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Permission check: only project owner or manager can create tasks
    if current_user.id != db_project.owner_id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not authorized to add tasks to this project")

    # Create the task in DB
    new_task = task_service.create_task(db=db, task=task, project_id=project_id)

    # Schedule background email notification
    background_tasks.add_task(
        send_email,
        recipients=[current_user.email],  # or task.assigned_to email
        subject="New Task Assigned",
        body=f"Task '{task.title}' has been assigned!"
    )

    return new_task


@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    db_project = project_service.get_project(db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user is assigned or involved in the project
    # (optional, you can add RBAC logic here)
    tasks = task_service.get_tasks(db, project_id=project_id, skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    db_task = task_service.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Optional: permission check
    return db_task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    project_id: int,
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    db_task = task_service.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Permission check
    db_project = project_service.get_project(db, project_id=project_id)
    if current_user.id != db_project.owner_id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    return task_service.update_task(db=db, task_id=task_id, task=task)


@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    db_task = task_service.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Permission check
    db_project = project_service.get_project(db, project_id=project_id)
    if current_user.id != db_project.owner_id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    return task_service.delete_task(db=db, task_id=task_id)