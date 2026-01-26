from pydantic import BaseModel
from typing import Optional

# ===================== ROOM MODELS =====================

class RoomCreate(BaseModel):
    room_number: str
    room_type: str  # Single, Double, Suite
    price_per_night: float
    is_available: bool = True

class Room(BaseModel):
    id: int
    room_number: str
    room_type: str
    price_per_night: float
    is_available: bool = True

    class Config:
        from_attributes = True

class UpdateRoomModel(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    price_per_night: Optional[float] = None
    is_available: Optional[bool] = None

# ===================== GUEST MODELS =====================

class GuestCreate(BaseModel):
    name: str
    email: str
    phone: str

class Guest(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        from_attributes = True

class UpdateGuestModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

# ===================== BOOKING MODELS =====================

class BookingCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    total_price: float
    status: str = "confirmed"

class Booking(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    total_price: float
    status: str = "confirmed"

    class Config:
        from_attributes = True

class UpdateBookingModel(BaseModel):
    guest_id: Optional[int] = None
    room_id: Optional[int] = None
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
