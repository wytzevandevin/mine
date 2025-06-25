from pydantic import BaseModel

class BaseSchema(BaseModel):
    id: int

    class Config:
        from_attributes = True 