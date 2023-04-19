from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from sqlalchemy.sql.functions import func
from models.Place import Place, Opinion
from database import get_db, engine

router = APIRouter(
    prefix="/places",
    tags=['Places']
)

paginate_by = 50


@router.get("/list-in-radius/{radius}/{lat}/{lon}", response_model=List[schemas.Place])
def get_places_in_radius(radius: float, lon: float, lat: float, page: int = 1, db: Session = Depends(get_db)):
    offset = (page - 1) * paginate_by
    center = func.ST_Point(lon, lat)
    places = db.query(Place).filter(Place.published == True, func.ST_DWithin(Place.location, center, radius)).order_by(
        Place.avg_score()).offset(offset).limit(paginate_by).all()

    # TODO odegosc i sort po odleglosci
    return places


@router.get("/list-in-radius-category/{category}/{radius}/{lat}/{lon}", response_model=List[schemas.Place])
def get_places_in_radius_category(category: str, radius: float, lon: float, lat: float, page: int = 1,
                                  db: Session = Depends(get_db)):
    offset = (page - 1) * paginate_by
    center = func.ST_Point(lon, lat)
    places = db.query(Place).filter(Place.published == True, Place.category == category,
                                    func.ST_DWithin(Place.location, center, radius)).order_by(Place.location).offset(
        offset).limit(paginate_by).all()

    # TODO odegosc i sort po odleglosci
    return places


@router.get("/list", response_model=List[schemas.Place])
def get_places(page: int = 1, db: Session = Depends(get_db)):
    offset = (page - 1) * paginate_by
    return db.query(Place).filter(Place.published == True).offset(offset).limit(paginate_by).all()


@router.post("/list", response_model=schemas.Place)
async def create_places(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    place = Place(**place.dict())
    db.add(place)
    db.commit()
    return place


@router.get("/list-unpublished", response_model=List[schemas.Place])
async def get_unpublished_places(page: int = 1, db: Session = Depends(get_db)):
    offset = (page - 1) * paginate_by
    return db.query(Place).filter(Place.published == False).offset(offset).limit(paginate_by).all()


@router.get("/id/{uuid}", response_model=schemas.Place)
async def get_place(uuid, db: Session = Depends(get_db)):
    p = db.query(Place).filter(Place.id == uuid).first()
    # p.avg_score()
    return p


@router.patch("/id/{uuid}")
async def patch_place(uuid, data: schemas.PlaceEdit, db: Session = Depends(get_db)):
    # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                     detail="Not authorized to perform requested action")
    place = db.query(Place).filter(Place.id == uuid)
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"place with id: {uuid} does not exist")
    # if admin
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")

    place.update(data.dict(), synchronize_session=False)
    db.commit()
    return place.first()


@router.patch("/id/{uuid}")
async def delete_place(uuid, db: Session = Depends(get_db)):
    # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                     detail="Not authorized to perform requested action")
    place = db.query(Place).filter(Place.id == uuid).first()
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"place with id: {uuid} does not exist")
    # if admin
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")

    place.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
