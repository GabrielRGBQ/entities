from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import settings
from .database import engine
from .routers import authentication, entity, like, user

# Create the tables in the database if they don't already exist
# It is no longer needed since we incorporated Alembic... we can create the
# database by using Alembic comands
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Handle CORS policy
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(entity.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(like.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
