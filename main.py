from fastapi import FastAPI, Depends
from routers import place_router, category_router, opinion_router, user_router
from models import Place, Category, Opinion, User
from database import engine, get_db

Category.Base.metadata.create_all(bind=engine)
Place.Base.metadata.create_all(bind=engine)
Opinion.Base.metadata.create_all(bind=engine)
User.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(place_router.router)
app.include_router(category_router.router)
app.include_router(opinion_router.router)
app.include_router(user_router.router)

