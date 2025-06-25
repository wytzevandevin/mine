from sqlalchemy import Column, String, Boolean, INTEGER
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "nb_consoleusers"

    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    node = Column(INTEGER, nullable=False)
    permission = Column(String, nullable=False)