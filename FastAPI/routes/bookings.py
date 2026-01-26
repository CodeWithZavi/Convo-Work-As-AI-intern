from fastapi import APIRouter, HTTPException
from models import Booking, UpdateBookingModel
from database import bookings, rooms

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

# ===================== BOOKING ENDPOINTS =====================

@router.get("")
def get_bookings():
    return bookings

@router.get("/{booking_id}")
def get_booking(booking_id: int):
    for booking in bookings:
        if booking.id == booking_id:
            return booking
    raise HTTPException(status_code=404, detail="Booking not found")

@router.post("")
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

@router.put("/{booking_id}")
def update_booking(booking_id: int, update: UpdateBookingModel):
    for booking in bookings:
        if booking.id == booking_id:
            if update.guest_id is not None:
                booking.guest_id = update.guest_id
            if update.room_id is not None:
                booking.room_id = update.room_id
            if update.check_in_date is not None:
                booking.check_in_date = update.check_in_date
            if update.check_out_date is not None:
                booking.check_out_date = update.check_out_date
            if update.total_price is not None:
                booking.total_price = update.total_price
            if update.status is not None:
                booking.status = update.status
            return booking
    raise HTTPException(status_code=404, detail="Booking not found")

@router.delete("/{booking_id}")
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
