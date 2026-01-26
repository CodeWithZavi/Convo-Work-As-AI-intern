from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import GuestCreate, UpdateGuestModel
from db_models import GuestDB
from db_config import get_db

router = APIRouter(prefix="/api/guests", tags=["guests"])

# ===================== GUEST ENDPOINTS =====================

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
    
    db_guest = GuestDB(
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
    
    # Check if guest has active bookings
    from db_models import BookingDB
    active_bookings = db.query(BookingDB).filter(
        BookingDB.guest_id == guest_id,
        BookingDB.status.in_(["confirmed", "checked-in"])
    ).count()
    
    if active_bookings > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete guest with active bookings"
        )
    
    db.delete(guest)
    db.commit()
    return {"message": "Guest deleted successfully", "id": guest_id}
