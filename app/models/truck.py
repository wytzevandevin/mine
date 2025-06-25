from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Truck(BaseModel):
    __tablename__ = "nb_unit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    alias = Column(String, unique=True, nullable=False)
    mine = Column(Integer, nullable=False)  # in tons
    type = Column(Integer, nullable=False)
    category = Column(Integer, nullable=True)

    # ⬇️ Add this relationship
    assignment = relationship("Assign", back_populates="truck", uselist=False, cascade="all, delete-orphan")

    # Shortcut relationships to digger and dump through assignment
    digger = relationship("Digger", secondary="nb_unit_assign", primaryjoin="Truck.id==Assign.truck_id",
                          secondaryjoin="Assign.digger_id==Digger.id", viewonly=True, uselist=False)
    dump = relationship("Dump", secondary="nb_unit_assign", primaryjoin="Truck.id==Assign.truck_id",
                        secondaryjoin="Assign.dump_id==Dump.id", viewonly=True, uselist=False)