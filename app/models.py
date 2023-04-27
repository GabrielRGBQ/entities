from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.sql.expression import text
from .database import Base

class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))