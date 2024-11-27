from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from app import app
from app.models import *
from app.forms import ReservationForm, WaitingListForm


# Route for reserving a table
@app.route('/', methods=['GET', 'POST'])
def home():

    form = ReservationForm()
    form.location.choices = Restaurant.query.order_by(Restaurant.id)
    if form.validate_on_submit():
        # Form was successfully submitted and validated
        date = form.date.data
        time = form.time.data
        party_size = form.party_size.data
        customer_name = form.customer_name.data
        customer_phone = form.customer_phone.data
        Seating.query.filter_by()
        # add_booking()

        # Process the data (e.g., save it to the database or perform other logic)
        # Flash a success message and redirect to a success page
        flash(f"Reservation made for {customer_name} at {time} on {date} for {party_size} people.", "success")

    return render_template('index.html', form=form)


@app.route('/waiting', methods=['GET', 'POST'])
def wait():
    form = WaitingListForm()
    form.location.choices = Restaurant.query.order_by(Restaurant.id)
    if form.validate_on_submit():
        date = form.date.data
        time = form.time.data
        party_size = form.party_size.data
        customer_name = form.customer_name.data
        customer_phone = form.customer_phone.data
        
        # Insert data into the waiting list
        add_to_waiting_list(customer_name, customer_phone)
        
        # Flash success message
        flash(f"Reservation for {customer_name} added to the waiting list for {date} at {time}.", "success")
        
        # Redirect to the same page or another page (optional)
        return redirect(url_for('wait'))
    
    return render_template('waiting.html', form=form)