from typing import List
from models import Room, Guest, Booking

# ===================== IN-MEMORY DATA STORAGE =====================

rooms: List[Room] = [
    Room(id=1, room_number="101", room_type="Single", price_per_night=100.0, is_available=True),
    Room(id=2, room_number="102", room_type="Double", price_per_night=150.0, is_available=True),
    Room(id=3, room_number="201", room_type="Suite", price_per_night=250.0, is_available=True),
    Room(id=4, room_number="202", room_type="Single", price_per_night=100.0, is_available=True),
]

guests: List[Guest] = []
bookings: List[Booking] = []
