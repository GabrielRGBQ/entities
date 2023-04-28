from fastapi import FastAPI, Depends, status
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routes import entity

# Create the tables in the database if they don't already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(entity.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
