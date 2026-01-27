from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import GuestCreate, UpdateGuestModel
from db_models import GuestDB
from db_config import get_db


@router.get("")
def get_guests(db: Session = Depends(get_db)):
    """Get all guests"""
    guests = db.query(GuestDB).all()
    return guests

@router.get("/{guest_id}")
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    """Get a specific guest by ID"""
    guest = db.query(GuestDB).filter(GuestDB.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

@router.post("")
def add_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    """Create a new guest"""
    # Check if email already exists
    existing_guest = db.query(GuestDB).filter(GuestDB.email == guest.email).first()
    if existing_guest:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Get the maximum ID and add 1 for new guest
    max_id = db.query(func.max(GuestDB.id)).scalar() or 0
    next_id = max_id + 1
    
    db_guest = GuestDB(
        id=next_id,
        name=guest.name,
        email=guest.email,
        phone=guest.phone
    )
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest

@router.put("/{guest_id}")
def update_guest(guest_id: int, update: UpdateGuestModel, db: Session = Depends(get_db)):
    """Update an existing guest"""
    guest = db.query(GuestDB).filter(GuestDB.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    # Update fields if provided
    if update.name is not None:
        guest.name = update.name
    if update.email is not None:
        # Check if new email conflicts with existing guest
        existing = db.query(GuestDB).filter(
            GuestDB.email == update.email,
            GuestDB.id != guest_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        guest.email = update.email
    if update.phone is not None:
        guest.phone = update.phone
    
    db.commit()
    db.refresh(guest)
    return guest

@router.delete("/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    """Delete a guest"""
    guest = db.query(GuestDB).filter(GuestDB.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    # Delete all bookings associated with this guest first
    from db_models import BookingDB, RoomDB
    bookings = db.query(BookingDB).filter(BookingDB.guest_id == guest_id).all()
    
    # Make rooms available again for deleted bookings
    for booking in bookings:
        room = db.query(RoomDB).filter(RoomDB.id == booking.room_id).first()
        if room:
            room.is_available = True
        db.delete(booking)
    
    # Delete the guest
    db.delete(guest)
    db.commit()
    
    # Reorder guest IDs sequentially after deletion
    remaining_guests = db.query(GuestDB).order_by(GuestDB.id).all()
    for index, guest_item in enumerate(remaining_guests, start=1):
        if guest_item.id != index:
            guest_item.id = index
    
    # Reorder booking IDs if any bookings were deleted
    if bookings:
        remaining_bookings = db.query(BookingDB).order_by(BookingDB.id).all()
        for index, booking_item in enumerate(remaining_bookings, start=1):
            if booking_item.id != index:
                booking_item.id = index
    
    db.commit()
    
    return {"message": "Guest and associated bookings deleted, IDs reordered successfully", "id": guest_id}
