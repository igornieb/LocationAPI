from pydantic import BaseModel


class PlaceBase(BaseModel):
    name: str
    description: str
    published: bool = False


class PlaceCreate(PlaceBase):
    pass


class PlaceEdit(PlaceBase):
    pass


class Place(PlaceBase):
    id: int

    class Config:
        orm_mode = True
