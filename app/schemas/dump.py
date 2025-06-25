from pydantic import BaseModel
from typing import Optional
from app.schemas.base import BaseSchema

class DumpOut(BaseModel):
    id: int
    name: str

class DumpIn(BaseModel):
    name: str