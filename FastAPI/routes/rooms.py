from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import RoomCreate, UpdateRoomModel
from db_models import RoomDB
from db_config import get_db

router = APIRouter(prefix="/api/rooms", tags=["rooms"])

# ===================== ROOM ENDPOINTS =====================

@router.get("")
def get_rooms(db: Session = Depends(get_db)):
    """Get all rooms"""
    rooms = db.query(RoomDB).all()
    return rooms

@router.get("/available")
def get_available_rooms(db: Session = Depends(get_db)):
    """Get all available rooms"""
    rooms = db.query(RoomDB).filter(RoomDB.is_available == True).all()
    return rooms

@router.get("/{room_id}")
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Get a specific room by ID"""
    room = db.query(RoomDB).filter(RoomDB.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("")
def add_room(room: RoomCreate, db: Session = Depends(get_db)):
    """Create a new room"""
    # Check if room number already exists
    existing_room = db.query(RoomDB).filter(RoomDB.room_number == room.room_number).first()
    if existing_room:
        raise HTTPException(status_code=400, detail="Room number already exists")
    
    # Get the maximum ID and add 1 for new room
    max_id = db.query(func.max(RoomDB.id)).scalar() or 0
    next_id = max_id + 1
    
    db_room = RoomDB(
        id=next_id,
        room_number=room.room_number,
        room_type=room.room_type,
        price_per_night=room.price_per_night,
        is_available=room.is_available
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.put("/{room_id}")
def update_room(room_id: int, update: UpdateRoomModel, db: Session = Depends(get_db)):
    """Update an existing room"""
    room = db.query(RoomDB).filter(RoomDB.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Update fields if provided
    if update.room_number is not None:
        # Check if new room number conflicts with existing room
        existing = db.query(RoomDB).filter(
            RoomDB.room_number == update.room_number,
            RoomDB.id != room_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Room number already exists")
        room.room_number = update.room_number
    
    if update.room_type is not None:
        room.room_type = update.room_type
    if update.price_per_night is not None:
        room.price_per_night = update.price_per_night
    if update.is_available is not None:
        room.is_available = update.is_available
    
    db.commit()
    db.refresh(room)
    return room

@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """Delete a room"""
    room = db.query(RoomDB).filter(RoomDB.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Delete all bookings associated with this room first
    from db_models import BookingDB
    bookings = db.query(BookingDB).filter(BookingDB.room_id == room_id).all()
    
    for booking in bookings:
        db.delete(booking)
    
    # Delete the room
    db.delete(room)
    db.commit()
    
    # Reorder room IDs sequentially after deletion
    remaining_rooms = db.query(RoomDB).order_by(RoomDB.id).all()
    for index, room_item in enumerate(remaining_rooms, start=1):
        if room_item.id != index:
            room_item.id = index
    
    # Reorder booking IDs if any bookings were deleted
    if bookings:
        remaining_bookings = db.query(BookingDB).order_by(BookingDB.id).all()
        for index, booking_item in enumerate(remaining_bookings, start=1):
            if booking_item.id != index:
                booking_item.id = index
    
    db.commit()
    
    return {"message": "Room and associated bookings deleted, IDs reordered successfully", "id": room_id}
    return {"message": "Room deleted successfully", "id": room_id}
