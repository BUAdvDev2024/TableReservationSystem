import unittest
from turtledemo.penrose import start

from flask import Flask
import os

from app import create_app, db
from app.models import Restaurant, Seating, Booking_slots, bookings
from datetime import time, datetime, timedelta


class TestConfig:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    WTF_CSRF_ENABLED = False

class TestFlaskAPIRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()

        # Add bookings to the database
        cls.restaurantName ='Test Restaurant 2'
        cls.booking_slot_date = datetime.strptime('2024-12-15', '%Y-%m-%d').date()
        cls.booking_slot_date_2 = datetime.strptime('2024-12-18', '%Y-%m-%d').date()
        cls.booking_slot_start_time = datetime.strptime('12:00:00', '%H:%M:%S').time()
        cls.booking_slot_end_time = datetime.strptime('13:00:00', '%H:%M:%S').time()
        with cls.app.app_context():
            restaurant = Restaurant(name=cls.restaurantName, address='123 Test St')
            db.session.add(restaurant)
            db.session.commit()

            seating = Seating(restaurant_id=restaurant.id, capacity=4, table_number=1)
            db.session.add(seating)
            db.session.commit()

            booking_slot1 = Booking_slots(
                date=cls.booking_slot_date,
                start_time=cls.booking_slot_start_time,
                end_time=cls.booking_slot_end_time
            )
            booking_slot2 = Booking_slots(
                date=cls.booking_slot_date_2,
                start_time=cls.booking_slot_start_time,
                end_time=cls.booking_slot_end_time
            )
            db.session.add(booking_slot1)
            db.session.add(booking_slot2)
            db.session.commit()

            booking1 = bookings(
                seating_id=seating.id,
                booking_slots_id=booking_slot1.id,
                customer_name='John Doe',
                customer_number='1234567890'
            )
            booking2 = bookings(
                seating_id=seating.id,
                booking_slots_id=booking_slot2.id,
                customer_name='Jane Doe',
                customer_number='0987654321'
            )
            db.session.add(booking1)
            db.session.add(booking2)
            db.session.commit()


    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_restaurant(self):
        response = self.client.post('/api/restaurants/Test Restaurant/123 Test St')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Restaurant added successfully', response.get_json().get('message'))

    def test_remove_restaurant(self):
        with self.app.app_context():
            restaurant = Restaurant(name='To Remove', address='456 Remove St')
            db.session.add(restaurant)
            db.session.commit()
            restaurant = Restaurant.query.filter_by(name='To Remove').first()

        response = self.client.delete(f'/api/restaurants/{restaurant.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Restaurant deleted successfully', response.get_json().get('message'))

    def test_add_seating(self): ##############
        with self.app.app_context():
            restaurant = Restaurant(name='Seating Test', address='789 Test St')
            restaurant_id = restaurant.id
            db.session.add(restaurant)
            db.session.commit()
            restaurant = Restaurant.query.filter_by(name='Seating Test').first()

        response = self.client.post(f'/api/seatings/{restaurant.id}/4/1')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Seating added successfully', response.get_json().get('message'))

    def test_remove_seating(self): ################
        with self.app.app_context():
            restaurant = Restaurant(name='Seating Remove Test', address='321 Remove St')
            db.session.add(restaurant)
            db.session.commit()
            seating = Seating(restaurant_id=restaurant.id, capacity=4, table_number=2)
            db.session.add(seating)
            db.session.commit()
            seating = Seating.query.filter_by(restaurant_id=restaurant.id, capacity=4, table_number=2).first()

        response = self.client.delete(f'/api/seatings/{seating.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Seating deleted successfully', response.get_json().get('message'))

    def test_add_booking_slot(self):
        response = self.client.post('/api/booking_slots/2025-01-17/12:00:00/13:00:00')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Booking slot added successfully', response.get_json().get('message'))

    def test_remove_booking_slot(self): ####################
        with self.app.app_context():
            slot = Booking_slots(date=datetime.today(), start_time=time(14,0), end_time=time(15,0))
            db.session.add(slot)
            db.session.commit()
            slot = Booking_slots.query.filter_by(start_time=time(14,0)).first()

        response = self.client.delete(f'/api/booking_slots/{slot.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Booking slot deleted successfully', response.get_json().get('message'))

    def test_get_bookings_for_restaurant_after_date(self):
        with self.app.app_context():
            restaurant = Restaurant.query.filter_by(name=self.restaurantName).first()

        # Test retrieving bookings for a restaurant after a certain date
        response = self.client.get(f'/api/bookings/{restaurant.id}?after_date={self.booking_slot_date.strftime("%Y-%m-%d")}')
        self.assertEqual(response.status_code, 200)
        bookings_data = response.get_json()
        self.assertEqual(len(bookings_data), 1)
        self.assertEqual(bookings_data[0]['customer_name'], 'Jane Doe')

    def test_add_booking_api(self):
        with self.app.app_context():
            restaurant = Restaurant.query.filter_by(name=self.restaurantName).first()

        response = self.client.post('/api/bookings/addBooking', json={
            'party_size': 4,
            'date': '2025-01-15',
            'time': '12:00:00',
            'customer_name': 'John Doe',
            'customer_phone': '1234567890',
            'restaurant': restaurant.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Booking made successfully', response.get_json().get('message'))
        with self.app.app_context():
            booking = bookings.query.filter_by(customer_name='John Doe', customer_number='1234567890').first()
            db.session.delete(booking)
            db.session.commit()

    def test_remove_booking_api(self):
        with self.app.app_context():
            new_booking = bookings(seating_id=1, booking_slots_id=1, customer_name="John Doe", customer_number="1234567890")
            db.session.add(new_booking)
            db.session.commit()

            # Attempt to remove the booking
            response = self.client.post('/api/bookings/removeBooking/1/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Booking successfully removed.", response.get_json().get('message'))

    def test_add_booking_api_missing_parameter(self):
        with self.app.app_context():
            restaurant = Restaurant.query.filter_by(name=self.restaurantName).first()

        response = self.client.post('/api/bookings/addBooking', json={
            'party_size': 4,
            'date': '2025-01-17',
            'time': '12:00:00',
            'customer_name': 'John Doe',
            # 'customer_phone' is missing
            'restaurant': restaurant.id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing parameter', response.get_json().get('error'))



if __name__ == '__main__':
    unittest.main(verbosity=2)