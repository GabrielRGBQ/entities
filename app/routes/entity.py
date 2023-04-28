from fastapi import FastAPI, Depends, status, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/entities")
def test_db(db: Session = Depends(get_db)):
    entities = db.query(models.Entity).all()
    return {"data": entities}


@router.post("/entities", status_code=status.HTTP_201_CREATED)
def create_entities(entity: schemas.EntityCreate, db: Session = Depends(get_db)):
    new_entity = models.Entity(**entity.dict())
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)
    return {"data": new_entity}