from typing import List

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from deps import get_current_user
from models.Place import Place
from models.Opinion import Opinion
from database import get_db, engine
import schemas
from models.User import User

router = APIRouter(
    prefix="/opinion",
    tags=['Opinions']
)


@router.get("/place/id/{uuid}", response_model=List[schemas.Opinion])
async def opinion_list(uuid, db: Session = Depends(get_db)):
    return db.query(Opinion).filter(Opinion.place == uuid).order_by(desc(Opinion.created_on)).all()


@router.post("/place/id/{uuid}", response_model=schemas.Opinion)
async def opinion_add(uuid, data: schemas.OpinionBase, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == uuid)
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Place with uuid: {uuid} does not exist")
    opinion = Opinion(**data.dict())
    opinion.place = uuid
    opinion.created_by = user.id
    db.add(opinion)
    db.commit()
    return opinion


@router.get("/id/{uuid}", response_model=schemas.Opinion)
async def opinion_details(uuid, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    return db.query(Opinion).filter(Opinion.id == uuid).first()


@router.patch("/id/{uuid}", response_model=schemas.Opinion)
async def opinion_edit(uuid, data: schemas.OpinionBase, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    opinion = db.query(Opinion).filter(Opinion.id == uuid)
    if opinion.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"opinion with id: {uuid} does not exist")
    if user.is_admin or opinion.created_by == user.id:
        opinion.update(data.dict(), synchronize_session=False)
        db.commit()
        return opinion.first()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

@router.delete("/id/{uuid}")
async def opinion_delete(uuid, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    opinion = db.query(Opinion).filter(Opinion.id == uuid)
    if opinion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"opinion with id: {uuid} does not exist")
    if user.is_admin or opinion.created_by == user.id:
        opinion.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
