from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services import auth_service
from app import schemas

router = APIRouter(tags=["Auth"])

@router.post("/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(auth_service.get_db)):
    return auth_service.register_user(db=db, user=user)

@router.post("/auth/login", response_model=schemas.Token)
def login(form_data:  OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth_service.get_db)):
    return auth_service.login_for_access_token(db=db, form_data=form_data)

@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth_service.get_current_user)):
    return current_user