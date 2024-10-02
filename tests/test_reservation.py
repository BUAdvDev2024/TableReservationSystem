import unittest
import json
from app import app  

class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_reserve_table_success(self):
        response = self.app.post('/reserve', json={
            "date": "2024-10-01",
            "time": "18:00",
            "party_size": 4,
            "customer_name": "John Doe",
            "customer_phone": "1234567890"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Table reserved", response.get_data(as_text=True))

    def test_reserve_table_invalid_input(self):
        response = self.app.post('/reserve', json={
            "date": "2024-10-01",
            "time": "18:00"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
