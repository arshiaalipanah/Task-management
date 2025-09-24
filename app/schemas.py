from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .models import UserRole
import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.viewer

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class User(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    owner_id: int
    tasks: List['Task'] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    project_id: int
    assigned_to: Optional[int] = None
    status: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True