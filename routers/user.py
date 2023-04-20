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
from email_validator import validate_email, EmailNotValidError

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
    return user


@router.delete("/settings")
async def user_delete(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user.id)
    user.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/settings/password")
async def user_details(data: schemas.UserEdit, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user.id)
    data.password = hash_password(data.password)
    user.update(data.dict(), synchronize_session=False)
    db.commit()
    return user.first()


@router.patch("/settings/email")
async def set_user_email(data: schemas.UserEmailEdit, user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user.id)
    try:
        validate_email(data.email)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    user.update(data.dict(), synchronize_session=False)
    db.commit()
    return user.first()


@router.get("/list")
async def user_list(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.is_admin:
        return db.query(User).all()
    else:
        raise HTTPException(status_code=status.HTTP_403_BAD_REQUEST)


@router.get("/id/{id}", response_model=schemas.User)
async def user_admin_details(id: str, admin: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if admin.is_admin:
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return user
    else:
        raise HTTPException(status_code=status.HTTP_403_BAD_REQUEST)


@router.patch("/id/{id}")
async def user_admin_patch(id: str, data: schemas.UserAdminEdit, admin: User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if admin.is_admin:
        user = db.query(User).filter(User.id == id)
        user.update(**data.dict(), synchronize_session=False)
        db.commit()
        return user.first()
    else:
        raise HTTPException(status_code=status.HTTP_403_BAD_REQUEST)


@router.delete("/id/{id}")
async def user_admin_delete(id: str, admin: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if admin.is_admin:
        user = db.query(User).filter(User.id == id)
        user.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_BAD_REQUEST)
