## API Documentation

### Restaurants

#### Add a Restaurant
- **Endpoint**: `POST /api/restaurants/<name>/<address>`
- **Description**: Adds a new restaurant with the specified name and address.
- **Parameters**:
  - `name` (string, URL parameter): Name of the restaurant.
  - `address` (string, URL parameter): Address of the restaurant.
- **Responses**:
  - `201 Created`: Restaurant added successfully.
  - `400 Bad Request`: Name or address not provided.
  - `500 Internal Server Error`: Error adding restaurant.

#### Remove a Restaurant
- **Endpoint**: `DELETE /api/restaurants/<int:restaurant_id>`
- **Description**: Deletes the restaurant with the specified ID.
- **Parameters**:
  - `restaurant_id` (int, URL parameter): ID of the restaurant to delete.
- **Responses**:
  - `200 OK`: Restaurant deleted successfully.
  - `404 Not Found`: Restaurant not found.
  - `500 Internal Server Error`: Error deleting restaurant.

---

### Seatings

#### Add Seating
- **Endpoint**: `POST /api/seatings/<int:restaurant_id>/<int:capacity>/<int:table_number>`
- **Description**: Adds seating to a restaurant.
- **Parameters**:
  - `restaurant_id` (int, URL parameter): ID of the restaurant.
  - `capacity` (int, URL parameter): Seating capacity.
  - `table_number` (int, URL parameter): Table number.
- **Responses**:
  - `201 Created`: Seating added successfully.
  - `400 Bad Request`: Missing required parameters.
  - `500 Internal Server Error`: Error adding seating.

#### Remove Seating
- **Endpoint**: `DELETE /api/seatings/<int:seating_id>`
- **Description**: Removes seating with the given ID.
- **Parameters**:
  - `seating_id` (int, URL parameter): ID of the seating to remove.
- **Responses**:
  - `200 OK`: Seating deleted successfully.
  - `404 Not Found`: Seating not found.
  - `500 Internal Server Error`: Error deleting seating.

---

### Booking Slots

#### Add Booking Slot
- **Endpoint**: `POST /api/booking_slots/<date>/<start_time>/<end_time>`
- **Description**: Adds a new booking slot.
- **Parameters**:
  - `date` (string, URL parameter): Date in YYYY-MM-DD format.
  - `start_time` (string, URL parameter): Start time in HH:MM:SS format.
  - `end_time` (string, URL parameter): End time in HH:MM:SS format.
- **Responses**:
  - `201 Created`: Booking slot added successfully.
  - `400 Bad Request`: Missing required parameters.
  - `500 Internal Server Error`: Error adding booking slot.

#### Remove Booking Slot
- **Endpoint**: `DELETE /api/booking_slots/<int:slot_id>`
- **Description**: Removes a booking slot with the given ID.
- **Parameters**:
  - `slot_id` (int, URL parameter): ID of the booking slot to remove.
- **Responses**:
  - `200 OK`: Booking slot deleted successfully.
  - `404 Not Found`: Booking slot not found.
  - `500 Internal Server Error`: Error deleting booking slot.

---

### Bookings

#### Add a Booking
- **Endpoint**: `POST /api/bookings/addBooking`
- **Description**: Creates a new booking.
- **Request Body** (JSON):
  - `party_size` (int): Number of people for the booking.
  - `date` (string): Date in YYYY-MM-DD format.
  - `time` (string): Time in HH:MM:SS format.
  - `customer_name` (string): Name of the customer.
  - `customer_phone` (string): Phone number of the customer.
  - `restaurant` (int): ID of the restaurant for the booking.
- **Responses**:
  - `201 Created`: Booking made successfully.
  - `400 Bad Request`: Missing parameter or unavailable booking.
  - `500 Internal Server Error`: Error adding booking.

#### Get Bookings for a Restaurant
- **Endpoint**: `GET /api/bookings/<int:restaurant_id>`
- **Description**: Retrieves all bookings for a specified restaurant (optionally filtered by dates).
- **Parameters**:
  - `restaurant_id` (int, URL parameter): ID of the restaurant.
  - `after_date` (string, query parameter, optional): Filter bookings after a specific date in YYYY-MM-DD format.
- **Responses**:
  - `200 OK`: List of bookings.
  - `400 Bad Request`: Invalid date format.
  - `500 Internal Server Error`: Error retrieving bookings.

#### Remove a Booking
- **Endpoint**: `POST /api/bookings/removeBooking/<int:seating_id>/<int:booking_slots_id>`
- **Description**: Removes an existing booking based on seating id and booking_slot_id.
- **Request Body** (JSON):
- **Responses**:
  - `200 Created`: Booking deleted successfully.
  - `400 Bad Request`: Missing parameter or unavailable booking.
  - `500 Internal Server Error`: Error adding booking.

---

These endpoints allow for adding, deleting, and retrieving data related to restaurants, seatings, booking slots, and bookings in the system. Adjust the structure as needed for a more comprehensive documentation style fitting your standards or add additional details where applicable.
