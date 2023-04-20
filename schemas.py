import datetime
import uuid
from typing import Optional, List
from pydantic import BaseModel

from models.Place import Place


class PlaceBase(BaseModel):
    name: str
    description: str
    category: str
    latitude: float
    longitude: float


class PlaceCreate(PlaceBase):
    pass


class PlaceEdit(PlaceBase):
    pass

class PlaceAdminEdit(PlaceBase):
    published: bool = False

class Place(PlaceBase):
    id: uuid.UUID
    avg_score: float
    distance: float = None
    published: bool = False

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    category: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class OpinionBase(BaseModel):
    stars: int
    opinion: str


class OpinionCreate(OpinionBase):
    place: uuid.UUID


class Opinion(OpinionCreate):
    id: uuid.UUID
    created_on: datetime.datetime
    created_by: uuid.UUID

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str
    password: str


class UserEdit(BaseModel):
    password: str


class UserEmailEdit(BaseModel):
    email: str


class UserAdminEdit(BaseModel):
    is_admin: bool


class UserLogin(UserBase):
    password: str


class User(UserCreate):
    pass


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
