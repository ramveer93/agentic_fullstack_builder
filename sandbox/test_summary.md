```python
import unittest
from backend import Appointment, AppointmentManager

class TestAppointmentManager(unittest.TestCase):

    def setUp(self):
        self.manager = AppointmentManager()

    def test_book_appointment(self):
        result = self.manager.book_appointment('John Doe', 'Dr. Smith', '2024-10-15 10:00 AM')
        self.assertTrue(result)
        self.assertEqual(len(self.manager.current_appointments()), 1)

        # Try to double book
        result = self.manager.book_appointment('Jane Doe', 'Dr. Smith', '2024-10-15 10:00 AM')
        self.assertFalse(result)

    def test_view_appointments(self):
        self.manager.book_appointment('John Doe', 'Dr. Smith', '2024-10-15 10:00 AM')
        appointments = self.manager.view_appointments('Dr. Smith')
        self.assertEqual(len(appointments), 1)

    def test_cancel_appointment(self):
        self.manager.book_appointment('John Doe', 'Dr. Smith', '2024-10-15 10:00 AM')
        result = self.manager.cancel_appointment('John Doe', 'Dr. Smith', '2024-10-15 10:00 AM')
        self.assertTrue(result)
        self.assertEqual(len(self.manager.current_appointments()), 0)

        # Try to cancel a non-existing appointment
        result = self.manager.cancel_appointment('Jane Doe', 'Dr. Smith', '2024-10-15 10:00 AM')
        self.assertFalse(result)

    def test_list_doctors(self):
        doctors = self.manager.list_doctors()
        self.assertIn('Dr. Smith', doctors)
        self.assertIn('Dr. Jones', doctors)
        self.assertIn('Dr. Brown', doctors)

if __name__ == '__main__':
    unittest.main()
```