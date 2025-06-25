from pydantic import BaseModel


class TruckOut(BaseModel):
    id: int
    name: str
    alias: str
    mine: int
    type: int
    category: int

class TruckIn(BaseModel):
    name: str
    alias: str
    mine: int
    type: int
    # category: str