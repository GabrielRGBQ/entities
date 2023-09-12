from fastapi import FastAPI

from . import models
from .database import engine
from .routers import entity, user, authentication, like
from .config import settings

# Create the tables in the database if they don't already exist
# It is no longer needed since we incorporated Alembic... we can create the
# database by using Alembic comands
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(entity.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(like.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
