from typing import List, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.schemas.digger import DiggerCreate
from app.models.digger import Digger
from app.models.truck import Truck
from app.models.mine import Mine
from app.models.type import Type

router = APIRouter()

# class DiggerCreate(BaseModel):
#     name: str

def serialize_digger(digger: Digger, db: Session) -> Dict:
    return {
        "id": digger.id,
        "name": digger.name
    }

@router.get("/")
def list_digger(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> List[Dict]:
    """
    Retrieve trucks.
    """
    diggers = db.query(Digger).offset(skip).limit(limit).all()
    return [serialize_digger(digger, db) for digger in diggers]

@router.post("/")
def create_digger(
    *,
    db: Session = Depends(get_db),
    digger_in: DiggerCreate
) -> Response:
    """
    Create new digger.
    """
    # Check if name already exists
    digger = db.query(Digger).filter(Digger.name == digger_in.name).first()
    if digger:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A digger with this name already exists.",
        )
    
    digger = Digger(
        name=digger_in.name
    )
    db.add(digger)
    db.commit()
    db.refresh(digger)
    return Response(content="", status_code=status.HTTP_201_CREATED)

@router.put("/{digger_id}")
def update_truck(
    *,
    db: Session = Depends(get_db),
    digger_id: int,
    digger_in: DiggerCreate
) -> Response:
    """
    Update truck.
    """
    row = db.query(Digger).filter(Digger.id == digger_id).first()
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
    if digger_in.name is not None:
        row.name = digger_in.name
    
    db.add(row)
    db.commit()
    db.refresh(row)
    return Response(content="", status_code=status.HTTP_200_OK)

@router.delete("/{digger_id}")
def delete_truck(
    *,
    db: Session = Depends(get_db),
    digger_id: int,
) -> Response:
    """
    Delete truck.
    """
    truck = db.query(Digger).filter(Digger.id == digger_id).first()
    if not truck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Truck not found",
        )

    db.delete(truck)
    db.commit()
    return Response(content="", status_code=status.HTTP_200_OK)