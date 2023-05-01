from fastapi import FastAPI

from . import models
from .database import engine
from .routers import entity, user

# Create the tables in the database if they don't already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(entity.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
