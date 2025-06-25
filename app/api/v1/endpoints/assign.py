from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.database import get_db
from app.models.assign import Assign
from app.models.digger import Digger
from app.models.dump import Dump
from app.models.truck import Truck
from app.schemas.assign import AssignIn

router = APIRouter()

# class DiggerCreate(BaseModel):
#     name: str

def serialize_assign(assign: Assign, db: Session) -> Dict:
    digger = db.query(Digger).filter(Digger.id == assign.digger_id).first()
    dump = db.query(Dump).filter(Dump.id == assign.dump_id).first()
    return {
        "id": assign.id,
        "truck": {
            "id": db.query(Truck).filter(Truck.id == assign.truck_id).first().id,
            "name": db.query(Truck).filter(Truck.id == assign.truck_id).first().alias
        },
        "digger": {
            "id": digger.id if digger else None,
            "name": digger.name if digger else None
        },
        "dump": {
            "id": dump.id if dump else None,
            "name": dump.name if dump else None,
        }
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
    assigns = db.query(Assign).offset(skip).limit(limit).all()
    if len(assigns)>0:
        return [serialize_assign(assign, db) for assign in assigns]
    return []

@router.post("/")
def create_assignment(
    *,
    db: Session = Depends(get_db),
    assign_in: AssignIn
) -> Response:
    """
    Create new digger.
    """
    # Check if name already exists
    digger = db.query(Assign).filter(Assign.truck_id == assign_in.truck).first()
    if digger:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A digger with this name already exists.",
        )
    
    assign = Assign(
        truck_id=assign_in.truck,
        digger_id=assign_in.digger,
        dump_id=assign_in.dump,
    )
    db.add(assign)
    db.commit()
    db.refresh(assign)
    return Response(content="", status_code=status.HTTP_200_OK)

@router.put("/{assign_id}")
def update_truck(
    *,
    db: Session = Depends(get_db),
    assign_id: int,
    assign_in: AssignIn
) -> Response:
    """
    Update truck.
    """
    row = db.query(Assign).filter(Assign.id == assign_id).first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Truck not found",
        )

    # Update truck fields
    if assign_in.truck is not None:
        row.truck_id = assign_in.truck
    if assign_in.digger is not None:
        row.digger_id = assign_in.digger
    if assign_in.dump is not None:
        row.dump_id = assign_in.dump
    
    db.add(row)
    db.commit()
    db.refresh(row)
    return Response(content="", status_code=status.HTTP_200_OK)

@router.delete("/{assign_id}")
def delete_truck(
    *,
    db: Session = Depends(get_db),
    assign_id: int,
) -> Response:
    """
    Delete truck.
    """
    assign_row = db.query(Assign).filter(Assign.id == assign_id).first()
    if not assign_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Truck not found",
        )
    
    # result = serialize_truck(truck, db)
    db.delete(assign_row)
    db.commit()
    return Response(content="", status_code=status.HTTP_200_OK)