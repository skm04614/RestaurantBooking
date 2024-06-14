from typing import Optional


class Customer:
    def __init__(self,
                 name: str,
                 phone_number: str,
                 email: Optional[str] = None):
        self.__name = name
        self.__phone_number = phone_number
        self.__email = email

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @property
    def email(self) -> Optional[str]:
        return self.__email
