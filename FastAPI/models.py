from pydantic import BaseModel
from typing import Optional

# ===================== ROOM MODELS =====================

class Room(BaseModel):
    id: int
    room_number: str
    room_type: str  # Single, Double, Suite
    price_per_night: float
    is_available: bool = True

class UpdateRoomModel(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    price_per_night: Optional[float] = None
    is_available: Optional[bool] = None

# ===================== GUEST MODELS =====================

class Guest(BaseModel):
    id: int
    name: str
    email: str
    phone: str

class UpdateGuestModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

# ===================== BOOKING MODELS =====================

class Booking(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    total_price: float
    status: str = "confirmed"  # confirmed, checked-in, checked-out, cancelled

class UpdateBookingModel(BaseModel):
    guest_id: Optional[int] = None
    room_id: Optional[int] = None
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
