from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# In-memory storage for bookings (will need to change to db later)
bookings = []

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Route for reserving a table
@app.route('/reserve', methods=['POST'])
def reserve_table():
    data = request.get_json()

    # Validate that all required fields are present
    if not data or 'date' not in data or 'time' not in data or 'party_size' not in data or 'customer_name' not in data or 'customer_phone' not in data:
        return jsonify({"message": "Invalid input. All fields are required.", "status": "error"}), 400

    # Validate party size
    try:
        party_size = int(data['party_size']) 
    except ValueError:
        return jsonify({"message": "Party size must be a valid number", "status": "error"}), 400

    if party_size < 1 or party_size > 20:
        return jsonify({"message": "Party size must be between 1 and 20", "status": "error"}), 400

    # Check for existing bookings for the same phone number, time, and party size
    existing_booking = next((booking for booking in bookings 
                            if booking['date'] == data['date'] and 
                                booking['time'] == data['time'] and 
                                booking['customer_phone'] == data['customer_phone']), None)

    if existing_booking:
        return jsonify({"message": "This table is already reserved with the same details.", "status": "error"}), 400

    # Check for existing bookings for the same date and time
    count = sum(1 for booking in bookings if booking['date'] == data['date'] and booking['time'] == data['time'])

    # Limit to 20 bookings per date and time
    if count >= 20:
        return jsonify({"message": "No more available bookings for this date and time.", "status": "error"}), 400

    # Create a booking
    booking = {
        "date": data['date'],
        "time": data['time'],
        "party_size": party_size,
        "customer_name": data['customer_name'],
        "customer_phone": data['customer_phone'],
    }

    # Save booking to the in-memory list
    bookings.append(booking)
    
    # Print booking details
    print("Booking Details:")
    print(f"Date: {booking['date']}")
    print(f"Time: {booking['time']}")
    print(f"Party Size: {booking['party_size']}")
    print(f"Customer Name: {booking['customer_name']}")
    print(f"Customer Phone: {booking['customer_phone']}")
    
    return jsonify({"message": "Table reserved", "status": "success", "booking": booking})


# Route for checking availability
@app.route('/availability', methods=['POST'])
def check_availability():
    data = request.get_json()
    
    if not data or 'date' not in data or 'time' not in data:
        return jsonify({"message": "Invalid input", "status": "error"}), 400

    # Check for existing bookings
    count = sum(1 for booking in bookings if booking['date'] == data['date'] and booking['time'] == data['time'])

    if count >= 2:
        return jsonify({"available": False})

    return jsonify({"available": True})

if __name__ == "__main__":
    app.run(debug=True)
