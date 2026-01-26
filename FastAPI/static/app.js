// Global variables
let rooms = [];
let guests = [];
let bookings = [];
let nextRoomId = 5;
let nextGuestId = 1;
let nextBookingId = 1;

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    loadRooms();
    loadGuests();
    loadBookings();
});

// Tab Management
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');

    // Load data for the selected tab
    if (tabName === 'rooms') loadRooms();
    if (tabName === 'guests') loadGuests();
    if (tabName === 'bookings') loadBookings();
}

// ==================== ROOMS ====================

function showAddRoomForm() {
    document.getElementById('addRoomForm').style.display = 'block';
}

function hideAddRoomForm() {
    document.getElementById('addRoomForm').style.display = 'none';
    document.getElementById('roomNumber').value = '';
    document.getElementById('roomType').value = 'Single';
    document.getElementById('roomPrice').value = '';
}

async function loadRooms() {
    try {
        const response = await fetch('/api/rooms');
        rooms = await response.json();
        displayRooms();
    } catch (error) {
        console.error('Error loading rooms:', error);
        alert('Failed to load rooms');
    }
}

function displayRooms() {
    const container = document.getElementById('roomsList');

    if (rooms.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No rooms available</h3>
                <p>Add your first room to get started</p>
            </div>
        `;
        return;
    }

    container.innerHTML = rooms.map(room => `
        <div class="card">
            <h3>Room ${room.room_number}</h3>
            <div class="card-info"><strong>Type:</strong> ${room.room_type}</div>
            <div class="card-info"><strong>Price:</strong> $${room.price_per_night}/night</div>
            <span class="status-badge ${room.is_available ? 'status-available' : 'status-occupied'}">
                ${room.is_available ? '✓ Available' : '✗ Occupied'}
            </span>
            <div class="card-actions">
                <button class="btn btn-danger" onclick="deleteRoom(${room.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

async function addRoom(event) {
    event.preventDefault();

    const room = {
        id: nextRoomId++,
        room_number: document.getElementById('roomNumber').value,
        room_type: document.getElementById('roomType').value,
        price_per_night: parseFloat(document.getElementById('roomPrice').value),
        is_available: true
    };

    try {
        const response = await fetch('/api/rooms', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(room)
        });

        if (response.ok) {
            hideAddRoomForm();
            loadRooms();
            alert('Room added successfully!');
        }
    } catch (error) {
        console.error('Error adding room:', error);
        alert('Failed to add room');
    }
}

async function deleteRoom(roomId) {
    if (!confirm('Are you sure you want to delete this room?')) return;

    try {
        const response = await fetch(`/api/rooms/${roomId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadRooms();
            alert('Room deleted successfully!');
        }
    } catch (error) {
        console.error('Error deleting room:', error);
        alert('Failed to delete room');
    }
}

// ==================== GUESTS ====================

function showAddGuestForm() {
    document.getElementById('addGuestForm').style.display = 'block';
}

function hideAddGuestForm() {
    document.getElementById('addGuestForm').style.display = 'none';
    document.getElementById('guestName').value = '';
    document.getElementById('guestEmail').value = '';
    document.getElementById('guestPhone').value = '';
}

async function loadGuests() {
    try {
        const response = await fetch('/api/guests');
        guests = await response.json();
        displayGuests();
    } catch (error) {
        console.error('Error loading guests:', error);
        alert('Failed to load guests');
    }
}

function displayGuests() {
    const container = document.getElementById('guestsList');

    if (guests.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No guests registered</h3>
                <p>Add your first guest to get started</p>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${guests.map(guest => `
                    <tr>
                        <td>${guest.id}</td>
                        <td>${guest.name}</td>
                        <td>${guest.email}</td>
                        <td>${guest.phone}</td>
                        <td>
                            <button class="btn btn-danger" onclick="deleteGuest(${guest.id})">Delete</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

async function addGuest(event) {
    event.preventDefault();

    const guest = {
        id: nextGuestId++,
        name: document.getElementById('guestName').value,
        email: document.getElementById('guestEmail').value,
        phone: document.getElementById('guestPhone').value
    };

    try {
        const response = await fetch('/api/guests', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(guest)
        });

        if (response.ok) {
            hideAddGuestForm();
            loadGuests();
            alert('Guest added successfully!');
        }
    } catch (error) {
        console.error('Error adding guest:', error);
        alert('Failed to add guest');
    }
}

async function deleteGuest(guestId) {
    if (!confirm('Are you sure you want to delete this guest?')) return;

    try {
        const response = await fetch(`/api/guests/${guestId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadGuests();
            alert('Guest deleted successfully!');
        }
    } catch (error) {
        console.error('Error deleting guest:', error);
        alert('Failed to delete guest');
    }
}

// ==================== BOOKINGS ====================

function showAddBookingForm() {
    // Populate guest dropdown
    const guestSelect = document.getElementById('bookingGuest');
    guestSelect.innerHTML = '<option value="">Select a guest</option>' +
        guests.map(g => `<option value="${g.id}">${g.name}</option>`).join('');

    // Populate room dropdown with available rooms only
    const roomSelect = document.getElementById('bookingRoom');
    const availableRooms = rooms.filter(r => r.is_available);
    roomSelect.innerHTML = '<option value="">Select a room</option>' +
        availableRooms.map(r => `<option value="${r.id}">Room ${r.room_number} - ${r.room_type} ($${r.price_per_night}/night)</option>`).join('');

    document.getElementById('addBookingForm').style.display = 'block';
}

function hideAddBookingForm() {
    document.getElementById('addBookingForm').style.display = 'none';
    document.getElementById('bookingGuest').value = '';
    document.getElementById('bookingRoom').value = '';
    document.getElementById('checkInDate').value = '';
    document.getElementById('checkOutDate').value = '';
    document.getElementById('totalPrice').value = '';
}

async function loadBookings() {
    try {
        const response = await fetch('/api/bookings');
        bookings = await response.json();
        displayBookings();
    } catch (error) {
        console.error('Error loading bookings:', error);
        alert('Failed to load bookings');
    }
}

function displayBookings() {
    const container = document.getElementById('bookingsList');

    if (bookings.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No bookings yet</h3>
                <p>Create your first booking to get started</p>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Guest</th>
                    <th>Room</th>
                    <th>Check-in</th>
                    <th>Check-out</th>
                    <th>Total Price</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${bookings.map(booking => {
        const guest = guests.find(g => g.id === booking.guest_id);
        const room = rooms.find(r => r.id === booking.room_id);
        return `
                        <tr>
                            <td>${booking.id}</td>
                            <td>${guest ? guest.name : 'Unknown'}</td>
                            <td>${room ? `Room ${room.room_number}` : 'Unknown'}</td>
                            <td>${booking.check_in_date}</td>
                            <td>${booking.check_out_date}</td>
                            <td>$${booking.total_price}</td>
                            <td>${booking.status}</td>
                            <td>
                                <button class="btn btn-danger" onclick="cancelBooking(${booking.id})">Cancel</button>
                            </td>
                        </tr>
                    `;
    }).join('')}
            </tbody>
        </table>
    `;
}

async function addBooking(event) {
    event.preventDefault();

    const booking = {
        id: nextBookingId++,
        guest_id: parseInt(document.getElementById('bookingGuest').value),
        room_id: parseInt(document.getElementById('bookingRoom').value),
        check_in_date: document.getElementById('checkInDate').value,
        check_out_date: document.getElementById('checkOutDate').value,
        total_price: parseFloat(document.getElementById('totalPrice').value),
        status: 'confirmed'
    };

    try {
        const response = await fetch('/api/bookings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(booking)
        });

        if (response.ok) {
            hideAddBookingForm();
            loadBookings();
            loadRooms(); // Refresh rooms to update availability
            alert('Booking created successfully!');
        } else {
            const error = await response.json();
            alert(error.detail || 'Failed to create booking');
        }
    } catch (error) {
        console.error('Error creating booking:', error);
        alert('Failed to create booking');
    }
}

async function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking?')) return;

    try {
        const response = await fetch(`/api/bookings/${bookingId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadBookings();
            loadRooms(); // Refresh rooms to update availability
            alert('Booking cancelled successfully!');
        }
    } catch (error) {
        console.error('Error cancelling booking:', error);
        alert('Failed to cancel booking');
    }
}
