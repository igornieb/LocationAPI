from typing import List

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from deps import get_current_user
from models.Category import Category
from database import get_db, engine
import schemas
from models.User import User

router = APIRouter(
    prefix="/category",
    tags=['Categories']
)

paginate_by = 100


@router.get("/")
def get_all(db: Session = Depends(get_db), page: int = 1):
    offset = (page - 1) * paginate_by
    return db.query(Category).offset(offset).limit(paginate_by).all()


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user.is_admin:
        category = Category(**category.dict())
        db.add(category)
        db.commit()
        return category
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
