import uuid
from typing import Optional, List
from pydantic import BaseModel

from models.Place import Place


class PlaceBase(BaseModel):
    name: str
    description: str
    category: str
    published: bool = False
    latitude: float
    longitude: float


class PlaceCreate(PlaceBase):
    pass


class PlaceEdit(PlaceBase):
    pass


class Place(PlaceBase):
    id: uuid.UUID
    avg_score: float

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

    class Config:
        orm_mode = True
