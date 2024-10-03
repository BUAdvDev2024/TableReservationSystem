from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from sqlalchemy.exc import NoResultFound


bookings = sa.Table(
    'bookings',
    db.metadata,
    sa.Column('seating_id', sa.Integer, sa.ForeignKey('seating.id'),
              primary_key=True),
    sa.Column('booking_slots_id', sa.Integer, sa.ForeignKey('booking_slots.id'),
              primary_key=True),
)

class Seating(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    capacity: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)

    def __repr__(self):
        return '<Seating {a} - Capacity: {b}>'.format(a=self.username, b=self.capacity)


class Booking_slots(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    time_slot: so.Mapped[str] = so.mapped_column(sa.DateTime(), index=True,
                                                unique=True)

    def __repr__(self):
        return '<Seating {a} - Capacity: {b}>'.format(a=self.username, b=self.capacity)


def add_booking(seating_id: int, booking_slot_id: int, guests) -> Optional[str]:
    """
    Add a booking by associating a seating with a booking slot.

    :param seating_id: ID of the seating.
    :param booking_slot_id: ID of the booking slot.
    :return: A message indicating success or error.
    """
    session = db.session
    try:

        existing_booking = session.execute(
            sa.select([bookings])
            .where(bookings.c.seating_id == seating_id)
            .where(bookings.c.booking_slots_id == booking_slot_id)
        ).first()

        if existing_booking:
            return "Duplicate booking: This seating and booking slot combination already exists."

        # Retrieve the Seating and Booking_slots instances from the database
        seating = session.query(Seating).filter_by(id=seating_id).one()
        if seating.capacity < guests:
            return "There are more guests than seats at the table"
        booking_slot = session.query(Booking_slots).filter_by(id=booking_slot_id).one()

        # Insert into the 'bookings' table
        stmt = bookings.insert().values(seating_id=seating.id, booking_slots_id=booking_slot.id)
        session.execute(stmt)
        session.commit()

        return "Booking successfully added."

    except NoResultFound:
        session.rollback()
        return "Error: Seating or Booking Slot not found."

    except Exception as e:
        session.rollback()
        return f"Error occurred: {str(e)}"


def add_test_seating_data():
    # Create a list of seating capacities ranging from 2 to 8
    seating_capacities = [str(i) for i in range(2, 9)]  # Generates ['2', '3', '4', '5', '6', '7', '8']

    for capacity in seating_capacities:
        # Create a new Seating instance
        seating = Seating(capacity=capacity)

        # Add the seating to the session

        db.session.add(seating)

    # Commit the session to insert all the records into the database
    try:
        db.session.commit()
        print("Test seating data added successfully.")
    except Exception as e:
        db.session.rollback()  # Roll back if there's an error
        print(f"An error occurred: {e}")

# add_test_seating_data()
