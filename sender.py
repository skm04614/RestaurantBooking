from booking import Booking


class Sender:
    @classmethod
    def send(cls,
             booking: Booking) -> None:
        cls.send_email(booking)
        cls.send_sms(booking)

    @classmethod
    def send_email(cls,
                   booking: Booking) -> None:
        if booking.customer.email:
            print(f"Sending email to {booking.customer.email} for schedule at {booking.time}")

    @classmethod
    def send_sms(cls,
                 booking: Booking) -> None:
        print(f"Sending SMS to {booking.customer.phone_number} for schedule at {booking.time}")
