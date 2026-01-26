from fastapi import APIRouter, HTTPException, Depends #for route handling and error management and dependency injection
from sqlalchemy.orm import Session #for database session management
from models import BookingCreate, UpdateBookingModel #importing Pydantic models for booking creation and update
from db_models import BookingDB, RoomDB, GuestDB    #importing database models for bookings, rooms, and guests
from db_config import get_db #importing function to get database session

router = APIRouter(prefix="/api/bookings", tags=["bookings"]) #defining API router for bookings with specified prefix and tags

# ===================== BOOKING ENDPOINTS =====================

@router.get("")
def get_bookings(db: Session = Depends(get_db)):
    """Get all bookings"""
    bookings = db.query(BookingDB).all()
    return bookings

@router.get("/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking by ID"""
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("")
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking"""
    # Check if guest exists
    guest = db.query(GuestDB).filter(GuestDB.id == booking.guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    # Check if room exists and is available
    room = db.query(RoomDB).filter(RoomDB.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not room.is_available:
        raise HTTPException(status_code=400, detail="Room is not available")
    
    # Create booking
    db_booking = BookingDB(
        guest_id=booking.guest_id,
        room_id=booking.room_id,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        total_price=booking.total_price,
        status=booking.status
    )
    
    # Mark room as unavailable
    room.is_available = False
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.put("/{booking_id}")
def update_booking(booking_id: int, update: UpdateBookingModel, db: Session = Depends(get_db)):
    """Update an existing booking"""
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    old_room_id = booking.room_id
    
    # Update fields if provided
    if update.guest_id is not None:
        guest = db.query(GuestDB).filter(GuestDB.id == update.guest_id).first()
        if not guest:
            raise HTTPException(status_code=404, detail="Guest not found")
        booking.guest_id = update.guest_id
    
    if update.room_id is not None and update.room_id != old_room_id:
        # Check if new room is available
        new_room = db.query(RoomDB).filter(RoomDB.id == update.room_id).first()
        if not new_room:
            raise HTTPException(status_code=404, detail="Room not found")
        if not new_room.is_available:
            raise HTTPException(status_code=400, detail="Room is not available")
        
        # Free up old room
        old_room = db.query(RoomDB).filter(RoomDB.id == old_room_id).first()
        if old_room:
            old_room.is_available = True
        
        # Mark new room as unavailable
        new_room.is_available = False
        booking.room_id = update.room_id
    
    if update.check_in_date is not None:
        booking.check_in_date = update.check_in_date
    if update.check_out_date is not None:
        booking.check_out_date = update.check_out_date
    if update.total_price is not None:
        booking.total_price = update.total_price
    if update.status is not None:
        # If changing to checked-out or cancelled, make room available
        if update.status in ["checked-out", "cancelled"] and booking.status not in ["checked-out", "cancelled"]:
            room = db.query(RoomDB).filter(RoomDB.id == booking.room_id).first()
            if room:
                room.is_available = True
        booking.status = update.status
    
    db.commit()
    db.refresh(booking)
    return booking

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """Cancel/delete a booking"""
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Make room available again
    room = db.query(RoomDB).filter(RoomDB.id == booking.room_id).first()
    if room:
        room.is_available = True
    
    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled successfully", "id": booking_id}
