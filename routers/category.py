from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from models.Category import Category
from database import get_db, engine
import schemas

router = APIRouter(
    prefix="/category",
    tags=['Categories']
)

paginate_by = 100

#TODO protect routes

@router.get("/")
def get_all(db: Session = Depends(get_db), page: int = 1):
    offset = (page - 1) * paginate_by
    return db.query(Category).offset(offset).paginate_by(paginate_by) .all()

@router.post("/", response_model=schemas.Category)
def get_all(category:schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**category.dict())
    db.add(category)
    db.commit()
    return category