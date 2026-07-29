from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing frontend on different origin

# Mock database for rooms and bookings
# In a real application, this would be a persistent database (e.g., SQLite, PostgreSQL, MongoDB)
rooms_db = [
    {
        "id": "R001",
        "name": "Standard Single Room",
        "type": "Single",
        "price": 100,
        "description": "Cozy room for one person, with a comfortable single bed and basic amenities.",
        "image": "https://via.placeholder.com/300x200/ADD8E6/FFFFFF?text=Single+Room",
        "max_occupancy": 1,
        "bookings": [] # List of {"check_in": "YYYY-MM-DD", "check_out": "YYYY-MM-DD", "guest_name": "", "guest_email": ""}
    },
    {
        "id": "R002",
        "name": "Standard Double Room",
        "type": "Double",
        "price": 150,
        "description": "Spacious room with a double bed, suitable for couples. Includes a private bathroom.",
        "image": "https://via.placeholder.com/300x200/90EE90/FFFFFF?text=Double+Room",
        "max_occupancy": 2,
        "bookings": []
    },
    {
        "id": "R003",
        "name": "Deluxe Suite",
        "type": "Suite",
        "price": 300,
        "description": "Luxurious suite with a king-size bed, separate living area, and stunning city view.",
        "image": "https://via.placeholder.com/300x200/FFB6C1/FFFFFF?text=Deluxe+Suite",
        "max_occupancy": 2, # Can be adjusted for suites
        "bookings": []
    },
    {
        "id": "R004",
        "name": "Family Room",
        "type": "Family",
        "price": 250,
        "description": "Large room with two double beds, perfect for families traveling with children.",
        "image": "https://via.placeholder.com/300x200/FFD700/FFFFFF?text=Family+Room",
        "max_occupancy": 4,
        "bookings": []
    }
]

# Helper function to check if two date ranges overlap
# Assumes check-out date is exclusive (room is available on check-out day)
def dates_overlap(check_in1_str, check_out1_str, check_in2_str, check_out2_str):
    ci1 = datetime.strptime(check_in1_str, "%Y-%m-%d")
    co1 = datetime.strptime(check_out1_str, "%Y-%m-%d")
    ci2 = datetime.strptime(check_in2_str, "%Y-%m-%d")
    co2 = datetime.strptime(check_out2_str, "%Y-%m-%d")

    # Overlap occurs if (start1 < end2) AND (end1 > start2)
    # This means two bookings don't overlap if one's checkout is exactly the other's checkin
    return ci1 < co2 and co1 > ci2

@app.route('/api/rooms', methods=['GET'])
def get_all_rooms():
    """Returns a list of all rooms in the hotel."""
    return jsonify(rooms_db)

@app.route('/api/availability', methods=['POST'])
def check_availability():
    """
    Checks for available rooms based on provided check-in, check-out dates,
    number of guests, and optional room type preference.
    """
    data = request.json
    check_in_str = data.get('checkInDate')
    check_out_str = data.get('checkOutDate')
    guests = int(data.get('guests', 1))
    room_type_pref = data.get('roomType')

    if not check_in_str or not check_out_str:
        return jsonify({"error": "Check-in and check-out dates are required."}), 400

    try:
        check_in_date = datetime.strptime(check_in_str, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out_str, "%Y-%m-%d")
        if check_in_date >= check_out_date:
            return jsonify({"error": "Check-out date must be after check-in date."}), 400
        if check_in_date < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            return jsonify({"error": "Check-in date cannot be in the past."}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    available_rooms = []
    for room in rooms_db:
        # Filter by room type preference
        if room_type_pref and room_type_pref != "Any" and room_type_pref != room['type']:
            continue

        # Filter by guest capacity
        if guests > room['max_occupancy']:
            continue

        is_available = True
        for booking in room['bookings']:
            if dates_overlap(check_in_str, check_out_str, booking['check_in'], booking['check_out']):
                is_available = False
                break
        
        if is_available:
            available_rooms.append(room)

    return jsonify(available_rooms)

@app.route('/api/book', methods=['POST'])
def book_room():
    """Processes a room booking request."""
    data = request.json
    room_id = data.get('roomId')
    check_in_str = data.get('checkInDate')
    check_out_str = data.get('checkOutDate')
    guest_name = data.get('guestName')
    guest_email = data.get('guestEmail')

    if not all([room_id, check_in_str, check_out_str, guest_name, guest_email]):
        return jsonify({"error": "Missing booking details. All fields are required."}), 400

    try:
        check_in_date = datetime.strptime(check_in_str, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    for room in rooms_db:
        if room['id'] == room_id:
            # Re-check availability before booking to ensure no double-booking
            # in case another user booked it simultaneously (simplified logic)
            is_available = True
            for booking in room['bookings']:
                if dates_overlap(check_in_str, check_out_str, booking['check_in'], booking['check_out']):
                    is_available = False
                    break

            if is_available:
                room['bookings'].append({
                    "check_in": check_in_str,
                    "check_out": check_out_str,
                    "guest_name": guest_name,
                    "guest_email": guest_email,
                    "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                return jsonify({"message": f"Room {room_id} booked successfully!", "booking_details": data}), 201
            else:
                return jsonify({"error": "Room is no longer available for the selected dates."}), 409 # Conflict
    
    return jsonify({"error": "Room not found."}), 404

if __name__ == '__main__':
    # Run the Flask app on port 5000 in debug mode
    app.run(debug=True, port=5000)