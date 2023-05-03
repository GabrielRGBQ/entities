from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/entities", tags=["Entities"])


@router.get("/", response_model=List[schemas.EntityOut])
def get_entities(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    entities = db.query(models.Entity).all()
    return entities


@router.get("/{id}", response_model=schemas.EntityOut)
def get_entity(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    entity = db.query(models.Entity).filter(models.Entity.id == id).first()

    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity with id: {id} was not found",
        )

    return entity


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Entity)
def create_entity(entity: schemas.EntityCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    new_entity = models.Entity(**entity.dict())
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)
    return new_entity


@router.put("/{id}", response_model=schemas.Entity)
def update_entity(id: int, updated_entity: schemas.EntityCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    entity_query = db.query(models.Entity).filter(models.Entity.id == id)
    entity = entity_query.first()

    if entity == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity with id: {id} was not found",
        )

    entity_query.update(updated_entity.dict(), synchronize_session=False)
    db.commit()
    return entity_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entity(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    entity_query = db.query(models.Entity).filter(models.Entity.id == id)
    entity = entity_query.first()

    if entity == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity with id: {id} does not exist",
        )

    entity_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
