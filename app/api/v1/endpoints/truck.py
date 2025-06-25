from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from kombu.asynchronous.http import Response
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.database import get_db
from app.models.mine import Mine
from app.models.truck import Truck
from app.models.type import Type
from app.schemas.truck import TruckIn

router = APIRouter()

def serialize_truck(truck: Truck, db: Session) -> Dict:
    mine = db.query(Mine).filter(Mine.id == truck.mine).first()
    type = db.query(Type).filter(Type.id == truck.type).first()
    return {
        "id": truck.id,
        "name": truck.name,
        "alias": truck.alias,
        "mine": {
            'id': mine.id,
            'name': mine.name
        },
        "type": {
            'id': type.id,
            'name': type.name
        },
        "category": truck.category
    }

@router.get("/")
def list_trucks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Dict:
    """
    Retrieve trucks.
    """
    trucks = db.query(Truck).offset(skip).limit(limit).all()
    mines = db.query(Mine).all()
    types = db.query(Type).all()
    serialize_mines=[]
    serialize_types=[]
    for mine in mines:
        serialize_mines.append({
            'id': mine.id,
            'name': mine.name
        })
    for type in types:
        serialize_types.append({
            'id': type.id,
            'name': type.name
        })

    return {
        'trucks':[serialize_truck(truck, db) for truck in trucks],
        'mines': serialize_mines,
        'types': serialize_types
    }

@router.post("/")
def create_truck(
    *,
    db: Session = Depends(get_db),
    truck_in : TruckIn
) -> Response | Response:
    """
    Create new truck.
    """
    # Check if alias already exists
    truck = db.query(Truck).filter(Truck.name == truck_in.name).first()
    if truck:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A truck with this alias already exists.",
        )
    
    truck = Truck(
        name=truck_in.name,
        alias=truck_in.alias,
        mine=truck_in.mine,
        type=truck_in.type
        # category=category
    )
    db.add(truck)
    db.commit()
    db.refresh(truck)
    return Response(content="", status_code=status.HTTP_201_CREATED)

@router.put("/{truck_id}")
def update_truck(
    *,
    db: Session = Depends(get_db),
    truck_id: int,
    truck_in : TruckIn
) -> Response | Response:
    """
    Update truck.
    """
    truck = db.query(Truck).filter(Truck.id == truck_id).first()
    if not truck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Truck not found",
        )
    
    # Check if new alias already exists
    if truck_in.alias and truck_in.alias != truck.alias:
        existing_truck = db.query(Truck).filter(Truck.alias == truck_in.alias).first()
        if existing_truck:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A truck with this alias already exists.",
            )
    
    # Update truck fields
    if truck_in.name is not None:
        truck.name = truck_in.name
    if truck_in.alias is not None:
        truck.alias = truck_in.alias
    if truck_in.mine is not None:
        truck.mine = truck_in.mine
    if truck_in.type is not None:
        truck.type = truck_in.type
    # if truck_in.category is not None:
    #     truck.category = truck_in.category
    
    db.add(truck)
    db.commit()
    db.refresh(truck)
    return Response(content="", status_code=status.HTTP_200_OK)

@router.delete("/{truck_id}")
def delete_truck(
    *,
    db: Session = Depends(get_db),
    truck_id: int,
) -> Dict:
    """
    Delete truck.
    """
    truck = db.query(Truck).filter(Truck.id == truck_id).first()
    if not truck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Truck not found",
        )
    
    result = serialize_truck(truck, db)
    db.delete(truck)
    db.commit()
    return result 