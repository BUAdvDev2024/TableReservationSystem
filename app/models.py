from datetime import timedelta
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from sqlalchemy.exc import NoResultFound
from datetime import timedelta, datetime, time
import random


class Seating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, index=True)
    table_number = db.Column(db.Integer, index=True)

    # Many-to-One relationship: each Seating belongs to one restaurant
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship('Restaurant', back_populates='seatings')

    def __repr__(self):
        return '<Seating {a} - Capacity: {b}>'.format(a=self.id, b=self.capacity)


class Booking_slots(db.Model):
    __tablename__ = 'booking_slots'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)  # Date for the booking slot
    start_time = db.Column(db.Time, index=True)  # Start time of the slot
    end_time = db.Column(db.Time, index=True)  # End time of the slot

    def __repr__(self):
        return f'<BookingSlot {self.date} {self.start_time} - {self.end_time}>'

class Restaurant(db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    # Optional: other details like city, postal code, etc.

    # One-to-Many relationship with Seating
    seatings = db.relationship('Seating', back_populates='restaurant', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<restaurant {self.name}, Address: {self.address}>'


class bookings(db.Model):
    __tablename__ = 'bookings'

    seating_id = db.Column(db.Integer, db.ForeignKey('seating.id', name='fk_seating_id'), primary_key=True)
    booking_slots_id = db.Column(db.Integer, db.ForeignKey('booking_slots.id', name='fk_booking_slots_id'),
                                 primary_key=True)
    customer_name = db.Column(db.String)
    customer_number = db.Column(db.String)

    # Correct relationships - refer to the class 'Seating' and 'BookingSlot'
    seating = db.relationship('Seating', backref=db.backref('bookings', lazy='dynamic'))
    booking_slots = db.relationship('Booking_slots', backref=db.backref('bookings', lazy='dynamic'))

    def __repr__(self):
        return f'<Booking: Seating ID {self.seating_id}, Slot ID {self.booking_slots_id}>'


def add_booking(capacity_needed, booking_slot_id, customer_name, customer_number):
    """
    Add a booking by associating a seating with a booking slot.

    :param seating_id: ID of the seating.
    :param booking_slot_id: ID of the booking slot.
    :return: A message indicating success or error.
    """
    session = db.session
    possible_seating = Seating.query.filter_by(capacity=capacity_needed).all()
    booked = False
    for table in possible_seating:
        if not booked:
            try:
                booking_slot = session.query(Booking_slots).filter_by(id=booking_slot_id).one()
                existing_booking = bookings.query.filter_by(seating_id=table.id, booking_slots_id=booking_slot.id).first()

                if existing_booking:
                    return "Duplicate booking: This seating and booking slot combination already exists."

                # Insert into the 'bookings' table
                new_booking = bookings(seating_id=table.id, booking_slots_id=booking_slot.id, customer_name=customer_name, customer_number=customer_number)
                db.session.add(new_booking)
                db.session.commit()
                booked = True
                return "Booking successfully added."

            except NoResultFound:
                session.rollback()
                return "Error: Seating or Booking Slot not found."

            except Exception as e:
                session.rollback()
                return f"Error occurred: {str(e)}"

    if booked:
        return True
    else:
        return False


def generate_time_slots_for_day(day: datetime):
    """Generates 1-hour slots from 9 AM to 9 PM for a given day."""
    start_hour = 9
    end_hour = 21  # 9 PM
    slots = []

    for hour in range(start_hour, end_hour):
        start_time = time(hour, 0)  # Start at the full hour
        end_time = time(hour + 1, 0)  # End at the next full hour
        slots.append((start_time, end_time))

    return slots


def populate_booking_slots(start_date: datetime, num_days: int = 1):
    """Populate booking slots for multiple days, starting from `start_date`."""
    for day_offset in range(num_days):
        current_day = start_date + timedelta(days=day_offset)
        slots = generate_time_slots_for_day(current_day)

        for start_time, end_time in slots:
            # Check if the slot already exists to avoid duplication
            existing_slot = Booking_slots.query.filter_by(date=current_day, start_time=start_time).first()
            if not existing_slot:
                # Create a new booking slot entry
                slot = Booking_slots(date=current_day, start_time=start_time, end_time=end_time)
                db.session.add(slot)

    # Commit the slots to the database
    db.session.commit()

def add_test_restaurant_and_restaurant_data():
    restaurants_data = [
        {"name": "Downtown Restaurant", "address": "123 Main St, Downtown"},
        {"name": "Uptown Eatery", "address": "456 Elm St, Uptown"},
        {"name": "Midtown Cafe", "address": "789 Oak St, Midtown"}
    ]

    # Insert restaurants into the database
    for loc_data in restaurants_data:
        restaurant = Restaurant(name=loc_data["name"], address=loc_data["address"])
        db.session.add(restaurant)
    # Create a list of seating capacities ranging from 2 to 8
    seating_capacities = [str(i) for i in range(2, 9)]  # Generates ['2', '3', '4', '5', '6', '7', '8']
    restaurant_ids = Restaurant.query.order_by(Restaurant.id).all()
    for capacity in seating_capacities:
        # Create a new Seating instance
        random_restaurant_id = random.choice(restaurant_ids).id
        seating = Seating(capacity=capacity,restaurant_id=random_restaurant_id,table_number=random.randint(0,100))

        # Add the seating to the session

        db.session.add(seating)

def add_test_seating_data():
    # Create a list of seating capacities ranging from 2 to 8
    seating_capacities = [str(i) for i in range(2, 9)]  # Generates ['2', '3', '4', '5', '6', '7', '8']
    restaurant_ids = Restaurant.query().all()
    for capacity in seating_capacities:
        # Create a new Seating instance
        random_restaurant_id = random.choice(restaurant_ids)[0]
        seating = Seating(capacity=capacity,restaurant_id=random_restaurant_id)

        # Add the seating to the session

        db.session.add(seating)

    # Commit the session to insert all the records into the database
    try:
        db.session.commit()
        print("Test seating data added successfully.")
    except Exception as e:
        db.session.rollback()  # Roll back if there's an error
        print(f"An error occurred: {e}")



