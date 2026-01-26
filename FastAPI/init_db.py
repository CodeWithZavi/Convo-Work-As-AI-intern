"""
Database initialization script
Run this script to create all tables and seed initial data
"""

from db_config import engine, Base, SessionLocal
from db_models import RoomDB, GuestDB, BookingDB

def init_database():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")

def seed_data():
    """Seed initial data into the database"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_rooms = db.query(RoomDB).count()
        if existing_rooms > 0:
            print("⚠ Database already contains data. Skipping seed.")
            return
        
        print("Seeding initial data...")
        
        # Add sample rooms
        rooms = [
            RoomDB(room_number="101", room_type="Single", price_per_night=100.0, is_available=True),
            RoomDB(room_number="102", room_type="Double", price_per_night=150.0, is_available=True),
            RoomDB(room_number="201", room_type="Suite", price_per_night=250.0, is_available=True),
            RoomDB(room_number="202", room_type="Single", price_per_night=100.0, is_available=True),
        ]
        
        db.add_all(rooms)
        db.commit()
        
        print("✓ Seed data added successfully!")
        print(f"  - {len(rooms)} rooms created")
        
    except Exception as e:
        print(f"✗ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

def drop_all_tables():
    """Drop all tables (use with caution!)"""
    print("⚠ WARNING: This will delete all data!")
    response = input("Are you sure you want to drop all tables? (yes/no): ")
    if response.lower() == 'yes':
        Base.metadata.drop_all(bind=engine)
        print("✓ All tables dropped successfully!")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    print("=" * 50)
    print("Hotel Management System - Database Setup")
    print("=" * 50)
    
    init_database()
    seed_data()
    
    print("\n" + "=" * 50)
    print("Database setup complete!")
    print("=" * 50)
