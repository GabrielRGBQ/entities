from fastapi import FastAPI, Depends, status
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

# Create the tables in the database if they don't already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/entities")
def test_db(db: Session = Depends(get_db)):
    entities = db.query(models.Entity).all()
    return {"data": entities}


@app.post("/entities", status_code=status.HTTP_201_CREATED)
def create_entities(entity: schemas.EntityCreate, db: Session = Depends(get_db)):
    new_entity = models.Entity(**entity.dict())
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)
    return {"data": new_entity}
