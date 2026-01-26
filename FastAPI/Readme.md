# Hotel Management System - Quick Start

## ✅ What's Been Implemented

Your Hotel Management System now has **complete PostgreSQL database integration** with the following features:

### Backend (FastAPI + PostgreSQL)
- ✅ Full CRUD operations for Rooms, Guests, and Bookings
- ✅ SQLAlchemy ORM for database operations
- ✅ PostgreSQL database with proper relationships
- ✅ Foreign key constraints
- ✅ Auto-incrementing IDs
- ✅ Timestamp tracking (created_at, updated_at)
- ✅ Data validation and error handling
- ✅ Business logic (prevent deletion with active bookings, check room availability)

### Frontend
- ✅ Create, Read, Update, Delete operations for all entities
- ✅ Responsive UI with forms for all operations
- ✅ Real-time data refresh
- ✅ Error handling and user feedback

## 📋 Prerequisites

Before running the application, you need:

1. **PostgreSQL Database** - You must install and set up PostgreSQL
   - Download from: https://www.postgresql.org/download/
   - Or use Docker: `docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres`

2. **Python Packages** - SQLAlchemy and python-dotenv (already installed)

3. **PostgreSQL Python Driver** - You need to install one of these:
   - **Option A (Recommended for Windows):** Download pre-built psycopg2 wheel
     ```powershell
     pip install psycopg2
     ```
   - **Option B:** Use asyncpg (alternative driver)
     ```powershell
     pip install asyncpg
     ```

## 🚀 Setup Steps

### 1. Install PostgreSQL

**Windows:**
```powershell
# Download and install from https://www.postgresql.org/download/windows/
# Or use Chocolatey:
choco install postgresql
```

**Using Docker (All platforms):**
```powershell
docker run --name hotel-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=hotel_management -p 5432:5432 -d postgres
```

### 2. Configure Database Connection

Edit the `.env` file (already created):
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hotel_management
```

Update with your PostgreSQL credentials:
- Username (default: `postgres`)
- Password (your PostgreSQL password)
- Host (default: `localhost`)
- Port (default: `5432`)

### 3. Create Database

**Option A: Using psql command line:**
```powershell
psql -U postgres -c "CREATE DATABASE hotel_management;"
```

**Option B: Using pgAdmin:**
- Open pgAdmin
- Right-click "Databases" → Create → Database
- Name: `hotel_management`

**Option C: If using Docker:**
Database is already created with the name `hotel_management`

### 4. Install PostgreSQL Driver

**Recommended: Try this first**
```powershell
pip install psycopg2
```

**If that fails, download a pre-built wheel:**
1. Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg
2. Download the appropriate `.whl` file for your Python version
3. Install: `pip install path\to\downloaded\file.whl`

**Alternative: Use asyncpg instead**
If psycopg2 doesn't work, you can use asyncpg:
```powershell
pip install asyncpg
```

Then update `db_config.py` to use asyncpg dialect:
```python
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/hotel_management"
```

### 5. Initialize Database

Run the initialization script:
```powershell
cd FastAPI
python init_db.py
```

This will:
- Create all tables (rooms, guests, bookings)
- Add initial sample data (4 rooms)

### 6. Run the Application

```powershell
cd FastAPI
uvicorn main:app --reload
```

The application will be available at: **http://localhost:8000**

## 📁 New Files Created

```
FastAPI/
├── .env                    # Database configuration (your credentials)
├── .env.example           # Example configuration
├── db_config.py           # Database connection and session management
├── db_models.py           # SQLAlchemy ORM models
├── init_db.py             # Database initialization script
├── SETUP_GUIDE.md         # Detailed setup guide
├── models.py              # Updated with Create models
├── routes/
│   ├── rooms.py           # Updated with database operations
│   ├── guests.py          # Updated with database operations
│   └── bookings.py        # Updated with database operations
├── main.py                # Updated with database lifecycle
└── static/
    └── app.js             # Updated to work with database IDs
```

## 🗄️ Database Schema

### Tables

**rooms**
- id (PK, Auto-increment)
- room_number (Unique)
- room_type
- price_per_night
- is_available
- created_at
- updated_at

**guests**
- id (PK, Auto-increment)
- name
- email (Unique)
- phone
- created_at
- updated_at

**bookings**
- id (PK, Auto-increment)
- guest_id (FK → guests.id)
- room_id (FK → rooms.id)
- check_in_date
- check_out_date
- total_price
- status
- created_at
- updated_at

## 🔧 Troubleshooting

### "Could not connect to database"
- Ensure PostgreSQL is running
- Check your credentials in `.env`
- Verify database `hotel_management` exists

### "Microsoft Visual C++ required" (psycopg2 installation)
- Download pre-built wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/
- Or use asyncpg instead: `pip install asyncpg`

### "Module not found: psycopg2"
- Install: `pip install psycopg2`
- Or download wheel and install manually

### Database tables not created
- Run: `python init_db.py`
- Check PostgreSQL is running
- Verify DATABASE_URL in `.env`

## 📚 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## ✨ Features

- ✅ **Complete CRUD** for all entities
- ✅ **Database Persistence** - Data saved to PostgreSQL
- ✅ **Relationships** - Foreign keys between tables
- ✅ **Validation** - Prevents duplicate emails, room numbers
- ✅ **Business Logic** - Can't delete rooms/guests with active bookings
- ✅ **Auto-increment IDs** - Database handles ID generation
- ✅ **Timestamps** - Automatic created_at and updated_at
- ✅ **RESTful API** - Standard HTTP methods
- ✅ **Interactive UI** - Full-featured web interface

## 🎯 Next Steps

1. Install PostgreSQL (if not already)
2. Install psycopg2 or asyncpg
3. Configure `.env` file
4. Run `python init_db.py`
5. Run `uvicorn main:app --reload`
6. Open http://localhost:8000

## 📖 For More Details

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for comprehensive instructions.
