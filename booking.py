from datetime import datetime

from customer import Customer


class Booking:
    def __init__(self,
                 time: datetime,
                 size: int,
                 customer: Customer):
        self.__time = time
        self.__size = size
        self.__customer = customer

    @property
    def time(self):
        return self.__time

    @property
    def size(self) -> int:
        return self.__size

    @property
    def customer(self) -> Customer:
        return self.__customer
