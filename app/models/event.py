from sqlalchemy import Column, Integer, DateTime

from app.models.base import BaseModel


class Event(BaseModel):
    __tablename__ = "nb_event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mine = Column(Integer, nullable=False)
    operator = Column(Integer, nullable=False)
    unit = Column(Integer, nullable=False)
    stamp = Column(DateTime, nullable=False)
    payload = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    km = Column(Integer, nullable=False)