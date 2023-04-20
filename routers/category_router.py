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


@router.get("/", response_model=List[schemas.Category])
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

@router.patch("/{name}", response_model=schemas.Category)
def patch_category(name:str, data:schemas.CategoryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.is_admin:
        category = db.query(Category).filter(Category.category == name).first()
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        db.query(Category).filter(Category.category == name).update(data.dict())
        db.commit()
        db.refresh(category)
        return category
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.delete("/{name}", response_model=schemas.Category)
def delete_category(name:str, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user.is_admin:
        category = db.query(Category).filter(Category.category==name)
        if category.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        category.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
