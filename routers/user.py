from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from sqlalchemy.sql.functions import func
from models.User import User
from database import get_db, engine
from utilis import hash_password, verify_password

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

# TODO authentication

@router.post("/register")
def register_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first() is not None:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED)
    user = User(username=data.username, email=data.email, password=hash_password(data.password))
    db.add(user)
    db.commit()
    return user


@router.post("/login")
def login_user(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if verify_password(user.password, data.password):
        return user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

