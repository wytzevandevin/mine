from sqlalchemy import Column, String, Integer, Boolean
from app.models.base import BaseModel

class Digger(BaseModel):
    __tablename__ = "nb_diggers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)