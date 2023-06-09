from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    entity = db.query(models.Entity).filter(models.Entity.id == like.entity_id).first()
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Entity with id: {like.entity_id} does not exist")

    like_query = db.query(models.Like).filter(
        models.Like.entity_id == like.entity_id, models.Like.user_id == current_user.id)

    found_like = like_query.first()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy liked on entity {like.entity_id}")
        new_like = models.Like(entity_id=like.entity_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully added like"}
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")

        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted like"}