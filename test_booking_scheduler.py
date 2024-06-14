import io
import unittest
from datetime import datetime
from contextlib import redirect_stdout
from freezegun import freeze_time

from booking_scheduler import BookingScheduler
from booking import Booking
from customer import Customer


class BookingSchedulerTest(unittest.TestCase):
    def setUp(self):
        self._customer_with_phone_and_email = Customer("Sam", "010-1234-5678", "sam@gmail.com")
        self._customer_with_phone = Customer("Paul", "010-3434-5656")

    def test_invalid_booking_time(self):
        dt = datetime.strptime("24-06-14 03:14", "%y-%m-%d %H:%M")
        booking_scheduler = BookingScheduler(20)

        with self.assertRaises(ValueError):
            booking_scheduler.add_booking(Booking(dt, 2, self._customer_with_phone_and_email))

    def test_valid_booking_time(self):
        dt = datetime.strptime("24-06-14 03:00", "%y-%m-%d %H:%M")
        booking_scheduler = BookingScheduler(20)

        booking_scheduler.add_booking(Booking(dt, 2, self._customer_with_phone_and_email))

    def test_invalid_booking_capacity(self):
        dt = datetime.strptime("24-06-14 03:00", "%y-%m-%d %H:%M")
        limit = 5
        booking_scheduler = BookingScheduler(limit)

        booking_scheduler.add_booking(Booking(dt, limit, self._customer_with_phone_and_email))
        with self.assertRaises(ValueError):
            booking_scheduler.add_booking(Booking(dt, limit, self._customer_with_phone))

    def test_valid_booking_with_different_booking_hours(self):
        dt1 = datetime.strptime("24-06-14 03:00", "%y-%m-%d %H:%M")
        dt2 = datetime.strptime("24-06-14 04:00", "%y-%m-%d %H:%M")
        limit = 5
        booking_scheduler = BookingScheduler(limit)

        booking_scheduler.add_booking(Booking(dt1, limit, self._customer_with_phone_and_email))
        booking_scheduler.add_booking(Booking(dt2, limit, self._customer_with_phone))

    def test_sms(self):
        dt = datetime.strptime("24-06-14 03:00", "%y-%m-%d %H:%M")
        limit = 5
        booking_scheduler = BookingScheduler(10 * limit)

        with io.StringIO() as buf, redirect_stdout(buf):
            booking_scheduler.add_booking(Booking(dt, limit, self._customer_with_phone))
            contents = buf.getvalue()

        self.assertIn("SMS", contents)

    def test_no_email(self):
        dt = datetime.strptime("24-06-14 03:00", "%y-%m-%d %H:%M")
        limit = 5
        booking_scheduler = BookingScheduler(10 * limit)

        with io.StringIO() as buf, redirect_stdout(buf):
            booking_scheduler.add_booking(Booking(dt, limit, self._customer_with_phone))
            contents = buf.getvalue()

        self.assertNotIn("email", contents)

    def test_sms_and_email(self):
        dt = datetime.strptime("24-06-14 03:00", "%y-%m-%d %H:%M")
        limit = 5
        booking_scheduler = BookingScheduler(10 * limit)

        with io.StringIO() as buf, redirect_stdout(buf):
            booking_scheduler.add_booking(Booking(dt, limit, self._customer_with_phone_and_email))
            contents = buf.getvalue()

        self.assertIn("email", contents)

    @freeze_time("2024-06-09")
    def test_invalid_sunday_request(self):
        dt = datetime.strptime("24-06-14 03:00", "%y-%m-%d %H:%M")
        limit = 5
        booking_scheduler = BookingScheduler(10 * limit)

        with self.assertRaises(ValueError):
            booking_scheduler.add_booking(Booking(dt, limit, self._customer_with_phone_and_email))

    @freeze_time("2024-06-10")
    def test_valid_non_sunday_request(self):
        dt = datetime.strptime("24-06-14 03:00", "%y-%m-%d %H:%M")
        limit = 5
        booking_scheduler = BookingScheduler(10 * limit)

        booking_scheduler.add_booking(Booking(dt, limit, self._customer_with_phone_and_email))


if __name__ == '__main__':
    unittest.main()
