from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Assign(BaseModel):
    __tablename__ = "nb_unit_assign"

    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_id = Column(Integer, ForeignKey('nb_unit.id', ondelete="CASCADE"), nullable=False)  # in tons
    digger_id = Column(Integer, ForeignKey('nb_diggers.id'), nullable=False)
    dump_id = Column(Integer, ForeignKey('nb_dumps.id'), nullable=False)

    # ⬇️ Add these relationships
    truck = relationship("Truck", back_populates="assignment")
    digger = relationship("Digger")
    dump = relationship("Dump")