from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services import project_service, auth_service
from app import models, schemas

router = APIRouter(tags=["Projects"])

@router.post("/projects/", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.role_check("admin"))
):
    return project_service.create_project(db=db, project=project, user_id=current_user.id)

@router.get("/projects/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    projects = project_service.get_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(
    project_id: int,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    db_project = project_service.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    # Add logic to check if user is assigned to project
    return db_project

@router.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.role_check("admin"))
):
    return project_service.update_project(db=db, project_id=project_id, project=project)

@router.delete("/projects/{project_id}", response_model=schemas.Project)
def delete_project(
    project_id: int,
    db: Session = Depends(auth_service.get_db),
    current_user: models.User = Depends(auth_service.role_check("admin"))
):
    return project_service.delete_project(db=db, project_id=project_id)