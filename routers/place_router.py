from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from sqlalchemy import func
from models.Place import Place, Opinion
from database import get_db, engine
from deps import get_current_user
from models.User import User

router = APIRouter(
    prefix="/places",
    tags=['Places']
)

paginate_by = 50


@router.get("/list-in-radius/{radius}/{lat}/{lon}", response_model=List[schemas.Place])
def get_places_in_radius(radius: float, lon: float, lat: float, sort_by: str = 'avg_score_desc', page: int = 1,
                         db: Session = Depends(get_db)):
    offset = (page - 1) * paginate_by
    center = func.ST_Point(lon, lat)
    if sort_by == 'avg_score_asc':
        places = db.query(Place).filter(Place.published == True,
                                        func.ST_DWithin(Place.location, center, radius)).order_by(
            asc(Place.avg_score)).offset(offset).limit(paginate_by).all()
    if sort_by == 'avg_score_desc':
        places = db.query(Place).filter(Place.published == True,
                                        func.ST_DWithin(Place.location, center, radius)).order_by(
            desc(Place.avg_score)).offset(offset).limit(paginate_by).all()
    if sort_by == 'distance_asc':
        places = db.query(Place).filter(Place.published == True,
                                        func.ST_DWithin(Place.location, center, radius)).order_by(
            asc(func.ST_Distance(Place.location, center))).offset(offset).limit(paginate_by).all()
    if sort_by == 'distance_desc':
        places = db.query(Place).filter(Place.published == True,
                                        func.ST_DWithin(Place.location, center, radius)).order_by(
            desc(func.ST_Distance(Place.location, center))).offset(offset).limit(paginate_by).all()
    else:
        places = db.query(Place).filter(Place.published == True,
                                        func.ST_DWithin(Place.location, center, radius)).offset(offset).limit(
            paginate_by).all()
    for place in places:
        place.distance_from_point(lon, lat)
    return places


@router.get("/distance-between/{uuid}}/{lat}/{lon}")
def get_distance_between(uuid, lon: float, lat: float, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == uuid).first()
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    point = func.ST_Point(lon, lat)
    result = db.query(func.ST_Distance(Place.location, point)).first()
    return {"distance": result[0]}


@router.get("/list-in-radius-category/{category}/{radius}/{lat}/{lon}", response_model=List[schemas.Place])
def get_places_in_radius_category(category: str, radius: float, lon: float, lat: float, sort_by: str = 'avg_score_desc', page: int = 1, db: Session = Depends(get_db)):
    offset = (page - 1) * paginate_by
    center = func.ST_Point(lon, lat)

    if sort_by == 'avg_score_asc':
        places = db.query(Place).filter(Place.published == True, Place.category == category, func.ST_DWithin(Place.location, center, radius)).order_by(asc(Place.avg_score)).offset(offset).limit(paginate_by).all()
    if sort_by == 'avg_score_desc':
        places = db.query(Place).filter(Place.published == True,Place.category == category,
                                        func.ST_DWithin(Place.location, center, radius)).order_by(
            desc(Place.avg_score)).offset(offset).limit(paginate_by).all()
    if sort_by == 'distance_asc':
        places = db.query(Place).filter(Place.published == True,Place.category == category,
                                        func.ST_DWithin(Place.location, center, radius)).order_by(
            asc(func.ST_Distance(Place.location, center))).offset(offset).limit(paginate_by).all()
    if sort_by == 'distance_desc':
        places = db.query(Place).filter(Place.published == True,Place.category == category,
                                        func.ST_DWithin(Place.location, center, radius)).order_by(
            desc(func.ST_Distance(Place.location, center))).offset(offset).limit(paginate_by).all()
    else:
        places = db.query(Place).filter(Place.published == True,Place.category == category,
                                        func.ST_DWithin(Place.location, center, radius)).offset(offset).limit(
            paginate_by).all()

    return places


@router.get("/list", response_model=List[schemas.Place])
def get_places(page: int = 1, db: Session = Depends(get_db)):
    offset = (page - 1) * paginate_by
    return db.query(Place).filter(Place.published == True).offset(offset).limit(paginate_by).all()


@router.post("/list", response_model=schemas.Place)
async def create_places(place: schemas.PlaceCreate, user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    place = Place(**place.dict())
    place.published = False
    place.created_by = user.id
    db.add(place)
    db.commit()
    return place


@router.get("/list-unpublished", response_model=List[schemas.Place])
async def get_unpublished_places(page: int = 1, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.is_admin:
        offset = (page - 1) * paginate_by
        return db.query(Place).filter(Place.published == False).offset(offset).limit(paginate_by).all()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/unpublished/id/{uuid}", response_model=schemas.Place)
async def get_unpublished_place(uuid, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.is_admin:
        p = db.query(Place).filter(Place.id == uuid, Place.published == False).first()
        if p is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"place with id: {uuid} does not exist")
        return p
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.patch("/unpublished/id/{uuid}")
async def patch_unpublished_place(uuid, data: schemas.PlaceAdminEdit, user: User = Depends(get_current_user),
                                  db: Session = Depends(get_db)):
    if user.is_admin:
        place = db.query(Place).filter(Place.id == uuid, Place.published == False).first()
        if place is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"place with id: {uuid} does not exist")
        if user.is_admin or place.creator == user.id:
            db.query(Place).filter(Place.id == uuid, Place.published == False).update(data.dict())
            db.commit()
            db.refresh(place)
            return place
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete("/unpublished/id/{uuid}")
async def delete_place(uuid, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == uuid, Place.published==False)
    if place.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"place with id: {uuid} does not exist")
    if user.is_admin:
        place.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/id/{uuid}", response_model=schemas.Place)
async def get_place(uuid, db: Session = Depends(get_db)):
    p = db.query(Place).filter(Place.id == uuid, Place.published == True).first()
    if p is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"place with id: {uuid} does not exist")
    return p


@router.patch("/id/{uuid}")
async def patch_place(uuid, data: schemas.PlaceEdit, user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == uuid, Place.published == True).first()
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"place with id: {uuid} does not exist")
    if user.is_admin or place.creator == user.id:
        db.query(Place).filter(Place.id == uuid, Place.published == True).update(data.dict())
        db.commit()
        db.refresh(place)
        return place
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete("/id/{uuid}")
async def delete_place(uuid, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == uuid)
    if place.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"place with id: {uuid} does not exist")

    if user.is_admin:
        place.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
