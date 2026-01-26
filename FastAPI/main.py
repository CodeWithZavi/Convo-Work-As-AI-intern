from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from routes import rooms, guests, bookings
from db_config import engine, Base
from db_models import RoomDB, GuestDB, BookingDB

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    print("Starting up... Creating database tables if they don't exist")
    Base.metadata.create_all(bind=engine)
    print("✓ Database ready")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Hotel Management System",
    description="A comprehensive hotel management system with PostgreSQL database",
    version="2.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(rooms.router)
app.include_router(guests.router)
app.include_router(bookings.router)

# Home route
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "postgresql",
        "version": "2.0.0"
    }
