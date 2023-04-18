from fastapi import FastAPI
from routers import place
from models import Place
from database import engine

#TODO migrations, models, coordinates fields, opinions
Place.Base.metadata.create_all(bind=engine)
#

app = FastAPI()

app.include_router(place.router)
