from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from app import app
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
