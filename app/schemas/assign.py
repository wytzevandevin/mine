from pydantic import BaseModel
from typing import Optional
from app.schemas.base import BaseSchema

class AssignIn(BaseModel):
    truck: int
    digger: int
    dump: int