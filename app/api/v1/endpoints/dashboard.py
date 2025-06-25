from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event import Event
from app.models.truck import Truck

router = APIRouter()
@router.get("/")
def list_dump(
    db: Session = Depends(get_db),
) -> List[Dict]:
    """
    Retrieve trucks with logic to handle last-row payload = 0:
    - If last payload is 0, find last non-zero payload
    - Also get the next row ID after that (if available)
    """
    trucks = db.query(Truck).all()
    result: List[Dict] = []
    distance = 0
    for truck in trucks:
        events = db.query(Event).filter(Event.unit==truck.id).all()
        if events and len(events) > 0:
            last_event = events[-1]
            new_cycle_start_event = None
            cycle_dump_event = None
            if last_event.payload == 0 and len(events) > 0:
                for index, event in reversed(list(enumerate(events))):
                    if event.payload != 0 and events[index-1].payload == 0:
                        new_cycle_start_event = event
                        break
                    elif event.payload == 0 and events[index-1].payload != 0:
                        cycle_dump_event = event

                if new_cycle_start_event is None:
                    distance = 0
                elif new_cycle_start_event is not None and cycle_dump_event is None:
                    distance = last_event.km - new_cycle_start_event
                elif new_cycle_start_event is not None and cycle_dump_event is not None:
                    distance = cycle_dump_event.km - new_cycle_start_event.km

                result.append({
                    'truck': truck.id,
                    'truck_name': truck.alias,
                    'speed': last_event.speed,
                    'payload': last_event.payload,
                    'cycle_start_time': new_cycle_start_event.stamp if new_cycle_start_event else 0,
                    'dump_time': cycle_dump_event.stamp if cycle_dump_event else 0,
                    'current_time': last_event.stamp,
                    'current_km': last_event.km - cycle_dump_event.km if cycle_dump_event else 0,
                    'distance': distance,
                    'digger': truck.digger.name if truck.digger else None,
                    'dump': truck.dump.name if truck.dump else None
                })
            elif last_event.payload != 0 and len(events) > 0:
                for index, event in reversed(list(enumerate(events))):
                    if event.payload != 0 and events[index-1].payload == 0:
                        new_cycle_start_event = event
                    elif event.payload == 0 and events[index-1].payload != 0:
                        cycle_dump_event = events[index-1]
                        break

                if new_cycle_start_event is None:
                    distance = 0
                elif new_cycle_start_event is not None and cycle_dump_event is None:
                    distance = last_event.km - new_cycle_start_event
                elif new_cycle_start_event is not None and cycle_dump_event is not None:
                    distance = new_cycle_start_event.km - cycle_dump_event.km

                result.append({
                    'truck': truck.id,
                    'truck_name': truck.alias,
                    'speed': last_event.speed,
                    'payload': last_event.payload,
                    'cycle_start_time': new_cycle_start_event.stamp if new_cycle_start_event else 0,
                    'dump_time': cycle_dump_event.stamp if cycle_dump_event else 0,
                    'current_time': last_event.stamp,
                    'current_km': last_event.km - new_cycle_start_event.km if new_cycle_start_event else 0,
                    'distance': distance,
                    'digger': truck.digger.name if truck.digger else None,
                    'dump': truck.dump.name if truck.dump else None
                })

    return result

