from fastapi import APIRouter, HTTPException
from models import Guest, UpdateGuestModel
from database import guests

router = APIRouter(prefix="/api/guests", tags=["guests"])

# ===================== GUEST ENDPOINTS =====================

@router.get("")
def get_guests():
    return guests

@router.get("/{guest_id}")
def get_guest(guest_id: int):
    for guest in guests:
        if guest.id == guest_id:
            return guest
    raise HTTPException(status_code=404, detail="Guest not found")

@router.post("")
def add_guest(guest: Guest):
    guests.append(guest)
    return guest

@router.put("/{guest_id}")
def update_guest(guest_id: int, update: UpdateGuestModel):
    for guest in guests:
        if guest.id == guest_id:
            if update.name is not None:
                guest.name = update.name
            if update.email is not None:
                guest.email = update.email
            if update.phone is not None:
                guest.phone = update.phone
            return guest
    raise HTTPException(status_code=404, detail="Guest not found")

@router.delete("/{guest_id}")
def delete_guest(guest_id: int):
    for index, guest in enumerate(guests):
        if guest.id == guest_id:
            deleted_guest = guests.pop(index)
            return deleted_guest
    raise HTTPException(status_code=404, detail="Guest not found")
