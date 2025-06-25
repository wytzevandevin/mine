from pydantic import BaseModel
from typing import Optional
from app.schemas.base import BaseSchema

class DiggerOut(BaseModel):
    id: int
    name: str

class DiggerCreate(BaseModel):
    name: str