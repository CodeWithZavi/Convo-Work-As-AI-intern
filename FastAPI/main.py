from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import rooms, guests, bookings

app = FastAPI(title="Hotel Management System")

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
