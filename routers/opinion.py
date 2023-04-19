from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from models.Place import Place
from models.Opinion import Opinion
from database import get_db, engine
import schemas

router = APIRouter(
    prefix="/opinion",
    tags=['Opinions']
)


@router.get("/place/id/{uuid}")
async def opinion_list(uuid, db: Session = Depends(get_db)):
    return db.query(Opinion).filter(Opinion.place == uuid).all()


@router.post("/place/id/{uuid}", response_model=schemas.Opinion)
async def opinion_add(uuid, data: schemas.OpinionBase, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == uuid)
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Place with uuid: {uuid} does not exist")
    opinion = Opinion(**data.dict())
    opinion.place = uuid
    db.add(opinion)
    db.commit()
    return opinion


@router.get("/id/{uuid}")
async def opinion_details(uuid, db: Session = Depends(get_db)):
    # if admin
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    return db.query(Opinion).filter(Opinion.id == uuid).first()


@router.patch("/id/{uuid}")
async def opinion_edit(uuid, data: schemas.OpinionBase, db: Session = Depends(get_db)):
    # if admin
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    opinion = db.query(Opinion).filter(Opinion.id == uuid)
    if opinion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"opinion with id: {uuid} does not exist")

    opinion.update(data.dict(), synchronize_session=False)
    db.commit()
    return opinion.first()


@router.delete("/id/{uuid}")
async def opinion_delete(uuid, db: Session = Depends(get_db)):
    opinion = db.query(Opinion).filter(Opinion.id == uuid)
    if opinion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"opinion with id: {uuid} does not exist")

    opinion.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
