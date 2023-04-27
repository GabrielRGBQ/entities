from fastapi import FastAPI, Depends
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

# Create the tables in the database if they don't already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_db(db: Session = Depends(get_db)):
    entities = db.query(models.Entity).all()
    return {"data": entities}
