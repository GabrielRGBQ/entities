from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class EntityBase(BaseModel):
    title: str
    description: str


class EntityCreate(EntityBase):
    pass


class Entity(EntityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class EntityOut(Entity):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
