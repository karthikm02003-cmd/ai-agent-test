document.addEventListener('DOMContentLoaded', () => {
    // --- Configuration ---
    const backendBaseUrl = 'http://127.0.0.1:5000/api'; // Ensure this matches your Flask backend port

    // --- DOM Elements ---
    const availabilityForm = document.getElementById('availability-form');
    const checkInDateInput = document.getElementById('check-in');
    const checkOutDateInput = document.getElementById('check-out');
    const guestsInput = document.getElementById('guests');
    const roomTypeSelect = document.getElementById('room-type');
    const roomsList = document.getElementById('rooms-list');
    const noRoomsMessage = document.querySelector('.no-rooms-message'); // Initial message

    const bookingModal = document.getElementById('booking-modal');
    const closeButton = bookingModal.querySelector('.close-button');
    const modalRoomDetails = document.getElementById('modal-room-details');
    const bookingDetailsForm = document.getElementById('booking-details-form');
    const guestNameInput = document.getElementById('guest-name');
    const guestEmailInput = document.getElementById('guest-email');
    const bookingMessage = document.getElementById('booking-message');

    // --- State Variables ---
    let selectedRoom = null; // Stores details of the room currently being booked
    let selectedCheckInDate = null;
    let selectedCheckOutDate = null;

    // --- Date Input Logic ---
    const today = new Date();
    const todayISO = today.toISOString().split('T')[0]; // Format YYYY-MM-DD

    // Set min date for check-in to today
    checkInDateInput.setAttribute('min', todayISO);

    // Update check-out min date when check-in date changes
    checkInDateInput.addEventListener('change', () => {
        if (checkInDateInput.value) {
            const checkInDate = new Date(checkInDateInput.value);
            const nextDay = new Date(checkInDate);
            nextDay.setDate(checkInDate.getDate() + 1); // Check-out must be at least one day after check-in
            const nextDayISO = nextDay.toISOString().split('T')[0];
            checkOutDateInput.setAttribute('min', nextDayISO);

            // If check-out date becomes invalid, reset it to the next day
            if (checkOutDateInput.value && new Date(checkOutDateInput.value) <= checkInDate) {
                checkOutDateInput.value = nextDayISO;
            }
        }
    });
    // Initialize check-out min date in case check-in is pre-filled by browser
    if (checkInDateInput.value) {
        checkInDateInput.dispatchEvent(new Event('change'));
    } else {
        // If check-in is empty, make sure check-out also respects today as min
        checkOutDateInput.setAttribute('min', todayISO);
    }

    // --- Availability Form Submission ---
    availabilityForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const checkInDate = checkInDateInput.value;
        const checkOutDate = checkOutDateInput.value;
        const guests = guestsInput.value;
        const roomType = roomTypeSelect.value;

        if (!checkInDate || !checkOutDate) {
            alert('Please select both check-in and check-out dates.');
            return;
        }

        // Store selected dates globally for booking modal
        selectedCheckInDate = checkInDate;
        selectedCheckOutDate = checkOutDate;

        try {
            const response = await fetch(`${backendBaseUrl}/availability`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ checkInDate, checkOutDate, guests: parseInt(guests), roomType }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch availability.');
            }

            displayRooms(data); // `data` is the array of available rooms

        } catch (error) {
            console.error('Error checking availability:', error);
            roomsList.innerHTML = `<p class="no-rooms-message error">Error: ${error.message}. Please try again.</p>`;
        }
    });

    // --- Room Display Logic ---
    function displayRooms(rooms) {
        roomsList.innerHTML = ''; // Clear previous results
        if (rooms.length === 0) {
            roomsList.innerHTML = '<p class="no-rooms-message">No rooms available for the selected dates and criteria.</p>';
            return;
        }

        rooms.forEach(room => {
            const roomCard = document.createElement('div');
            roomCard.classList.add('room-card');
            roomCard.innerHTML = `
                <img src="${room.image}" alt="${room.name}">
                <div class="room-card-content">
                    <h3>${room.name}</h3>
                    <p>${room.description}</p>
                    <p class="price">$${room.price} <span>/ night</span></p>
                    <button class="btn btn-primary book-now-btn" data-room-id="${room.id}">Book Now</button>
                </div>
            `;
            roomsList.appendChild(roomCard);
        });

        // Add event listeners to newly created "Book Now" buttons
        document.querySelectorAll('.book-now-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                const roomId = e.target.dataset.roomId;
                selectedRoom = rooms.find(r => r.id === roomId);
                openBookingModal();
            });
        });
    }

    // --- Booking Modal Logic ---
    function openBookingModal() {
        if (!selectedRoom || !selectedCheckInDate || !selectedCheckOutDate) {
            alert('Please search for and select a room with valid dates first.');
            return;
        }

        // Populate modal with room and date details
        modalRoomDetails.innerHTML = `
            <h3>${selectedRoom.name}</h3>
            <p><strong>Type:</strong> ${selectedRoom.type}</p>
            <p><strong>Price:</strong> $${selectedRoom.price} / night</p>
            <p><strong>Check-in:</strong> ${selectedCheckInDate}</p>
            <p><strong>Check-out:</strong> ${selectedCheckOutDate}</p>
        `;
        bookingMessage.innerHTML = ''; // Clear previous messages
        bookingMessage.className = 'message'; // Reset message styling
        guestNameInput.value = ''; // Clear form fields
        guestEmailInput.value = '';

        bookingModal.classList.add('active'); // Show the modal
    }

    function closeBookingModal() {
        bookingModal.classList.remove('active'); // Hide the modal
        selectedRoom = null; // Clear selected room
        // Dates are kept as they might be used for re-searching availability
    }

    closeButton.addEventListener('click', closeBookingModal);
    // Close modal if user clicks outside of modal content
    window.addEventListener('click', (event) => {
        if (event.target === bookingModal) {
            closeBookingModal();
        }
    });

    // --- Booking Details Form Submission ---
    bookingDetailsForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const guestName = guestNameInput.value.trim();
        const guestEmail = guestEmailInput.value.trim();

        if (!guestName || !guestEmail) {
            bookingMessage.innerHTML = 'Please fill in your full name and email address.';
            bookingMessage.className = 'message error';
            return;
        }

        if (!selectedRoom || !selectedCheckInDate || !selectedCheckOutDate) {
            bookingMessage.innerHTML = 'Error: No room or dates selected for booking. Please try again from search.';
            bookingMessage.className = 'message error';
            return;
        }

        try {
            const response = await fetch(`${backendBaseUrl}/book`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    roomId: selectedRoom.id,
                    checkInDate: selectedCheckInDate,
                    checkOutDate: selectedCheckOutDate,
                    guestName,
                    guestEmail
                }),
            });

            const data = await response.json();

            if (response.ok) {
                bookingMessage.innerHTML = `Booking successful! ${data.message}`;
                bookingMessage.className = 'message success';
                // Automatically close modal and refresh room list after a short delay
                setTimeout(() => {
                    closeBookingModal();
                    // Trigger the availability form submission again to update the room list
                    // This reflects the newly booked room's availability state
                    availabilityForm.dispatchEvent(new Event('submit'));
                }, 2000); // 2 seconds delay
            } else {
                bookingMessage.innerHTML = `Booking failed: ${data.error || 'Something went wrong.'}`;
                bookingMessage.className = 'message error';
            }
        } catch (error) {
            console.error('Error booking room:', error);
            bookingMessage.innerHTML = `An unexpected error occurred: ${error.message}`;
            bookingMessage.className = 'message error';
        }
    });
});