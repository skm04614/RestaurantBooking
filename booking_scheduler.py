from datetime import datetime

from booking import Booking
from sender import Sender


class BookingScheduler:
    def __init__(self,
                 size_limit_per_time_slot: int):
        self.__size_limit_per_time_slot = size_limit_per_time_slot
        self.__bookings: list[Booking] = []

    def add_booking(self,
                    booking: Booking) -> None:
        # if datetime.now().weekday() == 6:  # 일요일에는 시스템을 오픈하지 않는다. datetime 모듈에서 일요일은 6.
        #     raise ValueError("Booking system is not available on Sunday")

        if booking.time.minute:
            raise ValueError("Booking should be on the hour.")

        total_size_in_time_slot = sum(b.size for b in self.__bookings
                                      if b.time == booking.time)
        if total_size_in_time_slot + booking.size > self.__size_limit_per_time_slot:
            raise ValueError("Number of people is over restaurant capacity per hour")

        self.__bookings.append(booking)
        Sender.send(booking)

    def has_booking(self,
                    booking) -> bool:
        return booking in self.__bookings
