from sqlalchemy import Column, String, Integer, Boolean
from app.models.base import BaseModel

class Type(BaseModel):
    __tablename__ = "nb_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)