from fastapi import APIRouter, HTTPException
from models import Room, UpdateRoomModel
from database import rooms

router = APIRouter(prefix="/api/rooms", tags=["rooms"])

# ===================== ROOM ENDPOINTS =====================

@router.get("")
def get_rooms():
    return rooms

@router.get("/available")
def get_available_rooms():
    return [room for room in rooms if room.is_available]

@router.get("/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room.id == room_id:
            return room
    raise HTTPException(status_code=404, detail="Room not found")

@router.post("")
def add_room(room: Room):
    rooms.append(room)
    return room

@router.put("/{room_id}")
def update_room(room_id: int, update: UpdateRoomModel):
    for room in rooms:
        if room.id == room_id:
            if update.room_number is not None:
                room.room_number = update.room_number
            if update.room_type is not None:
                room.room_type = update.room_type
            if update.price_per_night is not None:
                room.price_per_night = update.price_per_night
            if update.is_available is not None:
                room.is_available = update.is_available
            return room
    raise HTTPException(status_code=404, detail="Room not found")

@router.delete("/{room_id}")
def delete_room(room_id: int):
    for index, room in enumerate(rooms):
        if room.id == room_id:
            deleted_room = rooms.pop(index)
            return deleted_room
    raise HTTPException(status_code=404, detail="Room not found")
