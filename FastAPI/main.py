from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Hotel Management System")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Data Models
class Room(BaseModel):
    id: int
    room_number: str
    room_type: str  # Single, Double, Suite
    price_per_night: float
    is_available: bool = True

class Guest(BaseModel):
    id: int
    name: str
    email: str
    phone: str

class Booking(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    total_price: float
    status: str = "confirmed"  # confirmed, checked-in, checked-out, cancelled

# In-memory data storage
rooms: List[Room] = [
    Room(id=1, room_number="101", room_type="Single", price_per_night=100.0, is_available=True),
    Room(id=2, room_number="102", room_type="Double", price_per_night=150.0, is_available=True),
    Room(id=3, room_number="201", room_type="Suite", price_per_night=250.0, is_available=True),
    Room(id=4, room_number="202", room_type="Single", price_per_night=100.0, is_available=True),
]

guests: List[Guest] = []
bookings: List[Booking] = []

# Routes
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# Room endpoints
@app.get("/api/rooms")
def get_rooms():
    return rooms

@app.get("/api/rooms/available")
def get_available_rooms():
    return [room for room in rooms if room.is_available]

@app.get("/api/rooms/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room.id == room_id:
            return room
    raise HTTPException(status_code=404, detail="Room not found")

@app.post("/api/rooms")
def add_room(room: Room):
    rooms.append(room)
    return room

@app.put("/api/rooms/{room_id}")
def update_room(room_id: int, updated_room: Room):
    for index, room in enumerate(rooms):
        if room.id == room_id:
            rooms[index] = updated_room
            return updated_room
    raise HTTPException(status_code=404, detail="Room not found")

@app.delete("/api/rooms/{room_id}")
def delete_room(room_id: int):
    for index, room in enumerate(rooms):
        if room.id == room_id:
            deleted_room = rooms.pop(index)
            return deleted_room
    raise HTTPException(status_code=404, detail="Room not found")

# Guest endpoints
@app.get("/api/guests")
def get_guests():
    return guests

@app.post("/api/guests")
def add_guest(guest: Guest):
    guests.append(guest)
    return guest

@app.get("/api/guests/{guest_id}")
def get_guest(guest_id: int):
    for guest in guests:
        if guest.id == guest_id:
            return guest
    raise HTTPException(status_code=404, detail="Guest not found")

# Booking endpoints
@app.get("/api/bookings")
def get_bookings():
    return bookings

@app.post("/api/bookings")
def create_booking(booking: Booking):
    # Check if room is available
    for room in rooms:
        if room.id == booking.room_id:
            if not room.is_available:
                raise HTTPException(status_code=400, detail="Room is not available")
            room.is_available = False
            break
    else:
        raise HTTPException(status_code=404, detail="Room not found")
    
    bookings.append(booking)
    return booking

@app.put("/api/bookings/{booking_id}")
def update_booking(booking_id: int, updated_booking: Booking):
    for index, booking in enumerate(bookings):
        if booking.id == booking_id:
            bookings[index] = updated_booking
            return updated_booking
    raise HTTPException(status_code=404, detail="Booking not found")

@app.delete("/api/bookings/{booking_id}")
def cancel_booking(booking_id: int):
    for index, booking in enumerate(bookings):
        if booking.id == booking_id:
            # Make room available again
            for room in rooms:
                if room.id == booking.room_id:
                    room.is_available = True
                    break
            deleted_booking = bookings.pop(index)
            return deleted_booking
    raise HTTPException(status_code=404, detail="Booking not found")
