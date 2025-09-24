from sqlalchemy.orm import Session
from app import models, schemas, database
from utils.email import send_email
from fastapi import BackgroundTasks

def create_task(db: Session, task: schemas.TaskCreate, project_id: int):
    db_task = models.Task(**task.model_dump(), project_id=project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.project_id == project_id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = get_task(db, task_id)
    if db_task:
        for key, value in task.model_dump().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def create_task_with_notification(task_data, background_tasks: BackgroundTasks):
    db = database.SessionLocal()
    new_task = models.Task(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        assigned_to=task_data.assigned_to
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # schedule email (business logic)
    background_tasks.add_task(
        send_email,
        recipients=["user@example.com"],
        subject="New Task Assigned",
        body=f"Task '{new_task.title}' has been assigned!"
    )

    return new_task