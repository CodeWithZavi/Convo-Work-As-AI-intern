# Hotel Management System - PostgreSQL Setup Guide

This guide will help you set up and run the Hotel Management System with PostgreSQL database.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher installed and running
- pip (Python package manager)

## Step 1: Install PostgreSQL

### Windows
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Default port is `5432`

### macOS
```bash
brew install postgresql
brew services start postgresql
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

## Step 2: Create Database

Open PostgreSQL command line or pgAdmin and run:

```sql
CREATE DATABASE hotel_management;
```

Alternatively, using command line:

```bash
# Windows (PowerShell)
psql -U postgres -c "CREATE DATABASE hotel_management;"

# macOS/Linux
sudo -u postgres psql -c "CREATE DATABASE hotel_management;"
```

## Step 3: Configure Database Connection

1. Copy `.env.example` to `.env`:
   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. Edit `.env` file and update the database connection string:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database_name
   ```

   Example:
   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/hotel_management
   ```

   Replace:
   - `username`: Your PostgreSQL username (default: `postgres`)
   - `password`: Your PostgreSQL password
   - `host`: Database server host (default: `localhost`)
   - `port`: PostgreSQL port (default: `5432`)
   - `database_name`: Database name (use: `hotel_management`)

## Step 4: Install Python Dependencies

Navigate to the FastAPI directory and install required packages:

```bash
cd FastAPI
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- psycopg2-binary (PostgreSQL driver)
- python-dotenv (environment variables)
- Pydantic (data validation)

## Step 5: Initialize Database

Run the initialization script to create tables and seed initial data:

```bash
python init_db.py
```

You should see:
```
==================================================
Hotel Management System - Database Setup
==================================================
Creating database tables...
✓ Database tables created successfully!
Seeding initial data...
✓ Seed data added successfully!
  - 4 rooms created

==================================================
Database setup complete!
==================================================
```

## Step 6: Run the Application

Start the FastAPI server:

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The application will be available at: http://localhost:8000

## Step 7: Access the Application

1. Open your browser and navigate to: http://localhost:8000
2. You should see the Hotel Management System interface
3. The API documentation is available at: http://localhost:8000/docs

## Database Schema

### Tables Created

1. **rooms**
   - id (Primary Key, Auto-increment)
   - room_number (Unique)
   - room_type (Single, Double, Suite)
   - price_per_night
   - is_available
   - created_at
   - updated_at

2. **guests**
   - id (Primary Key, Auto-increment)
   - name
   - email (Unique)
   - phone
   - created_at
   - updated_at

3. **bookings**
   - id (Primary Key, Auto-increment)
   - guest_id (Foreign Key → guests.id)
   - room_id (Foreign Key → rooms.id)
   - check_in_date
   - check_out_date
   - total_price
   - status (confirmed, checked-in, checked-out, cancelled)
   - created_at
   - updated_at

## API Endpoints

### Rooms
- `GET /api/rooms` - Get all rooms
- `GET /api/rooms/available` - Get available rooms
- `GET /api/rooms/{id}` - Get specific room
- `POST /api/rooms` - Create new room
- `PUT /api/rooms/{id}` - Update room
- `DELETE /api/rooms/{id}` - Delete room

### Guests
- `GET /api/guests` - Get all guests
- `GET /api/guests/{id}` - Get specific guest
- `POST /api/guests` - Create new guest
- `PUT /api/guests/{id}` - Update guest
- `DELETE /api/guests/{id}` - Delete guest

### Bookings
- `GET /api/bookings` - Get all bookings
- `GET /api/bookings/{id}` - Get specific booking
- `POST /api/bookings` - Create new booking
- `PUT /api/bookings/{id}` - Update booking
- `DELETE /api/bookings/{id}` - Cancel booking

## Troubleshooting

### Connection Error
If you see a connection error:
1. Check if PostgreSQL is running
2. Verify your credentials in `.env` file
3. Ensure the database `hotel_management` exists
4. Check if the port 5432 is not blocked by firewall

### Module Not Found Error
Run: `pip install -r requirements.txt`

### Database Already Exists
If you want to reset the database:
```bash
python
>>> from init_db import drop_all_tables
>>> drop_all_tables()
>>> exit()
python init_db.py
```

### Check Database Connection
Test your connection:
```bash
python
>>> from db_config import engine
>>> engine.connect()
```

## Features

✅ Complete CRUD operations for Rooms, Guests, and Bookings
✅ PostgreSQL database with SQLAlchemy ORM
✅ Automatic table creation and migrations
✅ Data validation with Pydantic
✅ Foreign key relationships
✅ Automatic room availability management
✅ Prevents deletion of rooms/guests with active bookings
✅ RESTful API design
✅ Interactive Swagger documentation
✅ Responsive web interface

## Development

To make changes to the database schema:
1. Modify models in `db_models.py`
2. Drop existing tables (CAUTION: This deletes all data)
3. Run `python init_db.py` to recreate tables

## Production Deployment

For production deployment:
1. Use a production-grade PostgreSQL server
2. Update `.env` with production database credentials
3. Use environment variables instead of `.env` file
4. Run with: `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4`
5. Consider using a reverse proxy (nginx) and process manager (supervisord/systemd)

## Support

For issues or questions:
1. Check the logs in the terminal
2. Review the API docs at http://localhost:8000/docs
3. Verify database connection and credentials
