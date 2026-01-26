# from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from typing import List, Optional

# app = FastAPI(title="Hotel Management System")

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # ===================== MODELS =====================

# class Room(BaseModel):
#     id: int
#     room_number: str
#     room_type: str  # Single, Double, Suite
#     price_per_night: float
#     is_available: bool = True

# class UpdateRoomModel(BaseModel):
#     room_number: Optional[str] = None
#     room_type: Optional[str] = None
#     price_per_night: Optional[float] = None
#     is_available: Optional[bool] = None

# class Guest(BaseModel):
#     id: int
#     name: str
#     email: str
#     phone: str

# class UpdateGuestModel(BaseModel):
#     name: Optional[str] = None
#     email: Optional[str] = None
#     phone: Optional[str] = None

# class Booking(BaseModel):
#     id: int
#     guest_id: int
#     room_id: int
#     check_in_date: str
#     check_out_date: str
#     total_price: float
#     status: str = "confirmed"  # confirmed, checked-in, checked-out, cancelled

# class UpdateBookingModel(BaseModel):
#     guest_id: Optional[int] = None
#     room_id: Optional[int] = None
#     check_in_date: Optional[str] = None
#     check_out_date: Optional[str] = None
#     total_price: Optional[float] = None
#     status: Optional[str] = None

# # ===================== DATA STORAGE =====================

# rooms: List[Room] = [
#     Room(id=1, room_number="101", room_type="Single", price_per_night=100.0),
#     Room(id=2, room_number="102", room_type="Double", price_per_night=150.0),
#     Room(id=3, room_number="201", room_type="Suite", price_per_night=250.0),
#     Room(id=4, room_number="202", room_type="Single", price_per_night=100.0),
# ]

# guests: List[Guest] = []
# bookings: List[Booking] = []

# # ===================== ROUTES =====================

# # Home page
# @app.get("/")
# async def read_root():
#     return FileResponse("static/index.html")

# # ===================== ROOMS =====================

# @app.get("/api/rooms")
# def get_rooms():
#     return rooms

# @app.get("/api/rooms/available")
# def get_available_rooms():
#     return [room for room in rooms if room.is_available]

# @app.get("/api/rooms/{room_id}")
# def get_room(room_id: int):
#     for room in rooms:
#         if room.id == room_id:
#             return room
#     raise HTTPException(status_code=404, detail="Room not found")

# @app.post("/api/rooms")
# def add_room(room: Room):
#     if any(r.id == room.id for r in rooms):
#         raise HTTPException(status_code=400, detail="Room with this ID already exists")
#     rooms.append(room)
#     return room

# @app.put("/api/rooms/{room_id}")
# def update_room(room_id: int, update: UpdateRoomModel):
#     for room in rooms:
#         if room.id == room_id:
#             if update.room_number is not None:
#                 room.room_number = update.room_number
#             if update.room_type is not None:
#                 room.room_type = update.room_type
#             if update.price_per_night is not None:
#                 room.price_per_night = update.price_per_night
#             if update.is_available is not None:
#                 room.is_available = update.is_available
#             return {"message": "Room updated successfully", "room": room}
#     raise HTTPException(status_code=404, detail="Room not found")

# @app.delete("/api/rooms/{room_id}")
# def delete_room(room_id: int):
#     for index, room in enumerate(rooms):
#         if room.id == room_id:
#             deleted_room = rooms.pop(index)
#             return {"message": "Room deleted successfully", "room": deleted_room}
#     raise HTTPException(status_code=404, detail="Room not found")

# # ===================== GUESTS =====================

# @app.get("/api/guests")
# def get_guests():
#     return guests

# @app.get("/api/guests/{guest_id}")
# def get_guest(guest_id: int):
#     for guest in guests:
#         if guest.id == guest_id:
#             return guest
#     raise HTTPException(status_code=404, detail="Guest not found")

# @app.post("/api/guests")
# def add_guest(guest: Guest):
#     if any(g.id == guest.id for g in guests):
#         raise HTTPException(status_code=400, detail="Guest with this ID already exists")
#     guests.append(guest)
#     return guest

# @app.put("/api/guests/{guest_id}")
# def update_guest(guest_id: int, update: UpdateGuestModel):
#     for guest in guests:
#         if guest.id == guest_id:
#             if update.name is not None:
#                 guest.name = update.name
#             if update.email is not None:
#                 guest.email = update.email
#             if update.phone is not None:
#                 guest.phone = update.phone
#             return {"message": "Guest updated successfully", "guest": guest}
#     raise HTTPException(status_code=404, detail="Guest not found")

# # ===================== BOOKINGS =====================

# @app.get("/api/bookings")
# def get_bookings():
#     return bookings

# @app.post("/api/bookings")
# def create_booking(booking: Booking):
#     # Check if room exists and is available
#     for room in rooms:
#         if room.id == booking.room_id:
#             if not room.is_available:
#                 raise HTTPException(status_code=400, detail="Room is not available")
#             room.is_available = False
#             break
#     else:
#         raise HTTPException(status_code=404, detail="Room not found")
    
#     bookings.append(booking)
#     return booking

# @app.put("/api/bookings/{booking_id}")
# def update_booking(booking_id: int, update: UpdateBookingModel):
#     for booking in bookings:
#         if booking.id == booking_id:
#             if update.guest_id is not None:
#                 booking.guest_id = update.guest_id
#             if update.room_id is not None:
#                 # Free old room
#                 for room in rooms:
#                     if room.id == booking.room_id:
#                         room.is_available = True
#                         break
#                 # Assign new room if available
#                 new_room = next((r for r in rooms if r.id == update.room_id), None)
#                 if new_room is None or not new_room.is_available:
#                     raise HTTPException(status_code=400, detail="New room is not available")
#                 booking.room_id = update.room_id
#                 new_room.is_available = False
#             if update.check_in_date is not None:
#                 booking.check_in_date = update.check_in_date
#             if update.check_out_date is not None:
#                 booking.check_out_date = update.check_out_date
#             if update.total_price is not None:
#                 booking.total_price = update.total_price
#             if update.status is not None:
#                 booking.status = update.status
#             return {"message": "Booking updated successfully", "booking": booking}
#     raise HTTPException(status_code=404, detail="Booking not found")

# @app.delete("/api/bookings/{booking_id}")
# def cancel_booking(booking_id: int):
#     for index, booking in enumerate(bookings):
#         if booking.id == booking_id:
#             # Make room available again
#             for room in rooms:
#                 if room.id == booking.room_id:
#                     room.is_available = True
#                     break
#             deleted_booking = bookings.pop(index)
#             return {"message": "Booking cancelled successfully", "booking": deleted_booking}
#     raise HTTPException(status_code=404, detail="Booking not found")
