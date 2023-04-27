from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EntityBase(BaseModel):
    title: str
    description: str


# class EntityCreate(EntityBase):
#     pass

class Entity(EntityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# class EntityOut(BaseModel):
#     Post: Entity
#     votes: int

#     class Config:
#         orm_mode = True