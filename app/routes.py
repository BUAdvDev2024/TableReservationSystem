from datetime import datetime
from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from app import app, db
from app.models import Booking_slots, bookings, Seating, add_booking, Restaurant
from app.forms import ReservationForm


@app.route("/", methods=['GET', 'POST'])
def home():

    return render_template('base.html')

# Route for reserving a table
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():

    form = ReservationForm()
    if form.validate_on_submit():
        # Form was successfully submitted and validated
        date = form.date.data
        time = form.time.data
        party_size = form.party_size.data
        customer_name = form.customer_name.data
        customer_phone = form.customer_phone.data
        slot = Booking_slots.query.filter_by(date=date, start_time=time).first()
        booking_made = add_booking(capacity_needed=party_size, booking_slot_id=slot.id, customer_name=customer_name,
                                   customer_number=customer_phone)
        if booking_made:

            # Process the data (e.g., save it to the database or perform other logic)
            # Flash a success message and redirect to a success page
            flash(f"Reservation made for {customer_name} at {time} on {date} for {party_size} people.", "success")

            return redirect('/')
        else:
            flash("Booking has not been made due to availability, would you like to get added to the waiting list")
    return render_template('reservation.html', form=form)

@app.route('/api/<restaurant_id>/<date>')
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
