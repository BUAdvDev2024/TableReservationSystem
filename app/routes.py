from datetime import datetime
from flask import Flask, request, jsonify, redirect, url_for, render_template, flash, Blueprint
from app import db
from app.models import Booking_slots, bookings, Seating, add_booking, Restaurant
from app.forms import ReservationForm

routeBlueprint = Blueprint("app", __name__, template_folder="templates")

@routeBlueprint.route("/", methods=['GET', 'POST'])
def home():

    return render_template('base.html')

# Route for reserving a table
@routeBlueprint.route('/reserve', methods=['GET', 'POST'])
def reserve():

    form = ReservationForm()
    if form.validate_on_submit():
        # Form was successfully submitted and validated
        date = form.date.data
        time = form.time.data
        party_size = form.party_size.data
        customer_name = form.customer_name.data
        customer_phone = form.customer_phone.data
        restaurant = form.location.data

        booking_made = add_booking(capacity_needed=party_size, booking_date=date, booking_time=time, customer_name=customer_name,
                                   customer_number=customer_phone, restaurant=restaurant)
        if booking_made:

            # Process the data (e.g., save it to the database or perform other logic)
            # Flash a success message and redirect to a success page
            flash(f"Reservation made for {customer_name} at {time} on {date} for {party_size} people.", "success")

            return redirect('/')
        else:
            flash("Booking has not been made due to availability, would you like to get added to the waiting list")
    return render_template('reservation.html', form=form)

@routeBlueprint.route('/api/<int:restaurant_id>/<date>')
def get_unique_booking_slots_available(restaurant_id, date):

    try:
        # Parse the date from the URL
        date = datetime.strptime(date, "%d-%m-%Y").date()

        # Count the number of seatings for the restaurant
        seating_count = (
            db.session.query(Seating.id)
            .filter(Seating.restaurant_id == restaurant_id)
            .count()
        )

        # Query booking slots where the number of bookings is less than the seating count
        free_slots = (
            db.session.query(Booking_slots)
            .outerjoin(bookings, bookings.booking_slots_id == Booking_slots.id)
            .join(Seating, bookings.seating_id == Seating.id, isouter=True)
            .filter(Seating.restaurant_id == restaurant_id)
            .filter(Booking_slots.date == date)
            .group_by(Booking_slots.id)
            .having(db.func.count(bookings.seating_id) < seating_count)
            .all()
        )

        # Serialize the result as a list of dictionaries
        free_slots_serialized = [slot.to_dict() for slot in free_slots]

        return jsonify(free_slots_serialized), 200

    except ValueError:
        return jsonify({"error": "Invalid date format, expected DD-MM-YYYY"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routeBlueprint.route('/api/restaurants/<name>/<address>', methods=['POST'])
def add_restaurant(name, address):
    if not name or not address:
        return jsonify({"error": "Name and address are required."}), 400

    try:
        new_restaurant = Restaurant(name=name, address=address)
        db.session.add(new_restaurant)
        db.session.commit()
        return jsonify({"message": "Restaurant added successfully.", "id": new_restaurant.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@routeBlueprint.route('/api/restaurants/<int:restaurant_id>', methods=['DELETE'])
def remove_restaurant(restaurant_id):
    try:
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
        if not restaurant:
            return jsonify({"error": "Restaurant not found."}), 404

        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({"message": "Restaurant deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@routeBlueprint.route('/api/seatings/<int:restaurant_id>/<int:capacity>/<int:table_number>', methods=['POST'])
def add_seating(restaurant_id, capacity, table_number):

    if not restaurant_id or not capacity or not table_number:
        return jsonify({"error": "Restaurant ID, capacity, and table number are required."}), 400

    try:
        new_seating = Seating(restaurant_id=restaurant_id, capacity=capacity, table_number=table_number)
        db.session.add(new_seating)
        db.session.commit()
        return jsonify({"message": "Seating added successfully.", "id": new_seating.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@routeBlueprint.route('/api/seatings/<int:seating_id>', methods=['DELETE'])
def remove_seating(seating_id):
    try:
        seating = Seating.query.filter_by(id=seating_id).first()
        if not seating:
            return jsonify({"error": "Seating not found."}), 404

        db.session.delete(seating)
        db.session.commit()
        return jsonify({"message": "Seating deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@routeBlueprint.route('/api/booking_slots/<date>/<start_time>/<end_time>', methods=['POST'])
def add_booking_slot(date, start_time, end_time):

    if not date or not start_time or not end_time:
        return jsonify({"error": "Date, start time, and end time are required."}), 400

    try:
        new_slot = Booking_slots(
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            start_time=datetime.strptime(start_time, '%H:%M:%S').time(),
            end_time=datetime.strptime(end_time, '%H:%M:%S').time()
        )
        db.session.add(new_slot)
        db.session.commit()
        return jsonify({"message": "Booking slot added successfully.", "id": new_slot.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@routeBlueprint.route('/api/booking_slots/<int:slot_id>', methods=['DELETE'])
def remove_booking_slot(slot_id):
    try:
        slot = Booking_slots.query.filter_by(id=slot_id).first()
        if not slot:
            return jsonify({"error": "Booking slot not found."}), 404

        db.session.delete(slot)
        db.session.commit()
        return jsonify({"message": "Booking slot deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@routeBlueprint.route('/api/bookings/addBooking', methods=['POST'])
def add_booking_api():
    data = request.get_json()
    try:
        booking_made = add_booking(
            capacity_needed=data['party_size'],
            booking_date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            booking_time=datetime.strptime(data['time'], '%H:%M:%S').time(),
            customer_name=data['customer_name'],
            customer_number=data['customer_phone'],
            restaurant=data['restaurant']
        )
        if booking_made:
            return jsonify({"message": "Booking made successfully."}), 201
        else:
            return jsonify({"error": "Booking could not be made due to availability."}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routeBlueprint.route('/api/bookings/removeBooking/<int:seating_id>/<int:booking_slots_id>', methods=['POST'])
def remove_booking_api(seating_id,booking_slots_id):
    try:
        booking_to_remove = bookings.query.filter_by(seating_id=seating_id, booking_slots_id=booking_slots_id).first()
        if booking_to_remove:
            db.session.delete(booking_to_remove)
            db.session.commit()
            return jsonify({"message": "Booking successfully removed."}), 200
        else:
            return jsonify({"error": "Booking could not be removed as it was not found."}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New API route to get all bookings for a specific restaurant
@routeBlueprint.route('/api/bookings/<int:restaurant_id>', methods=['GET'])
def get_bookings_for_restaurant(restaurant_id):
    try:
        # Get the 'after_date' parameter from the query string
        after_date_str = request.args.get('after_date')
        if after_date_str:

            after_date = datetime.strptime(after_date_str, '%Y-%m-%d').date()

            booking_slots_for_date = Booking_slots.query.filter(Booking_slots.date >= after_date).all()
            booking_slot_ids = [slot.id for slot in booking_slots_for_date]

            seats_for_restaurant = Seating.query.filter_by(restaurant_id=restaurant_id).all()
            seating_ids = [seat.id for seat in seats_for_restaurant]

            bookings_list = bookings.query.filter(
                bookings.seating_id.in_(seating_ids),
                bookings.booking_slots_id.in_(booking_slot_ids)
            ).all()
        else:
            seats_for_restaurant = Seating.query.filter_by(restaurant_id=restaurant_id).all()
            seating_ids = [seat.id for seat in seats_for_restaurant]

            bookings_list = bookings.query.filter(
                bookings.seating_id.in_(seating_ids),
            ).all()

        bookings_serialized = [
            {
                "seating_id": booking.seating_id,
                "booking_slots_id": booking.booking_slots_id,
                "customer_name": booking.customer_name,
                "customer_number": booking.customer_number,
                "date": booking.booking_slots.date.strftime("%Y-%m-%d"),
                "start_time": booking.booking_slots.start_time.strftime("%H:%M:%S"),
                "end_time": booking.booking_slots.end_time.strftime("%H:%M:%S"),
            }
            for booking in bookings_list]
        return jsonify(bookings_serialized), 200
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

