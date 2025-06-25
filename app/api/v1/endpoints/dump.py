from importlib.resources import contents
from typing import List, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Response
from kombu.asynchronous.http import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette.responses import Response

from app.database import get_db
from app.schemas.dump import DumpIn
from app.models.dump import Dump

router = APIRouter()

# class DiggerCreate(BaseModel):
#     name: str

def serialize_dump(dump: Dump, db: Session) -> Dict:
    return {
        "id": dump.id,
        "name": dump.name
    }

@router.get("/")
def list_dump(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> List[Dict]:
    """
    Retrieve trucks.
    """
    dumps = db.query(Dump).offset(skip).limit(limit).all()
    return [serialize_dump(dump, db) for dump in dumps]

@router.post("/")
def create_dump(
    *,
    db: Session = Depends(get_db),
    dump_in: DumpIn
) -> Response | Response:
    """
    Create new digger.
    """
    # Check if name already exists
    row = db.query(Dump).filter(Dump.name == dump_in.name).first()
    if row:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A digger with this name already exists.",
        )
    
    new_dump = Dump(
        name=dump_in.name
    )
    db.add(new_dump)
    db.commit()
    db.refresh(new_dump)
    return Response(content="", status_code=status.HTTP_201_CREATED)

@router.put("/{dump_id}")
def update_truck(
    *,
    db: Session = Depends(get_db),
    dump_id: int,
    dump_in: DumpIn
) -> Response | Response:
    """
    Update truck.
    """
    row = db.query(Dump).filter(Dump.id == dump_id).first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Truck not found",
        )
    
    # Check if new alias already exists
    # if alias and alias != truck.alias:
    #     existing_truck = db.query(Truck).filter(Truck.alias == alias).first()
    #     if existing_truck:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="A truck with this alias already exists.",
    #         )

    # Update truck fields
    if dump_in.name is not None:
        row.name = dump_in.name
    
    db.add(row)
    db.commit()
    db.refresh(row)
    return Response(content=dump_in.name, status_code=status.HTTP_200_OK)

@router.delete("/{dump_id}")
def delete_truck(
    *,
    db: Session = Depends(get_db),
    dump_id: int,
) -> Response | Response:
    """
    Delete truck.
    """
    dump_row = db.query(Dump).filter(Dump.id == dump_id).first()
    if not dump_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Truck not found",
        )
    db.delete(dump_row)
    db.commit()
    return Response(content="", status_code=status.HTTP_200_OK)