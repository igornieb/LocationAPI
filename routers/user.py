from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from sqlalchemy.sql.functions import func
from models.User import User
from database import get_db, engine
from utilis import hash_password, verify_password, create_access_token, create_refresh_token
from deps import get_current_user


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

# TODO authentication

@router.post("/register")
async def register_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first() is not None:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED)
    user = User(username=data.username, email=data.email, password=hash_password(data.password))
    db.add(user)
    db.commit()
    return user


@router.post("/login")
async def login_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if verify_password(user.password, data.password):
        return {
            "access_token": create_access_token(user.username),
            "refresh_token": create_refresh_token(user.username),
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/settings")
async def user_details(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(user)
    return user

