import re
from datetime import datetime
from abc import ABC,abstractmethod


class Field(ABC):
    def __init__(self, value):
        self.__value = value
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self) -> str:
        return f"{self.value}"

    def __eq__(self, other_obj: object) -> bool:
        if self.value == other_obj.value:
            return True
        else:
            return False


class Name(Field):
    def __init__(self, name: str) -> None:
        self.correct_name = name

    @property
    def correct_name(self):
        return self.value

    @correct_name.setter
    def correct_name(self, value):
        if not value or re.search(r"\W", value):
            raise ValueError(f"Invalid name format: {value}. Try again.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, number: str) -> None:
        self.correct_phone = number

    @property
    def correct_phone(self):
        return super().value

    @correct_phone.setter
    def correct_phone(self, phone: str | object) -> None:
        phone = str(phone)
        if self._phone_check(phone):
            raise ValueError(f'Phone {phone} is not right, must be only numbers')
        super().__init__(phone)
    
    def _phone_check(self, phone_number):

        if phone_number.startswith("+"):
            phone_number = phone_number[1:]

        not_number = re.search(r'\D', phone_number)

        if not_number:
            return True
        else:
            return False


class Email(Field):
    def __init__(self, email: str) -> None:
        self.correct_email = email

    @property
    def correct_email(self):
        return super().value

    @correct_email.setter
    def correct_email(self, email: str | object) -> None:
        email = str(email)
        if self._email_check(email):
            raise ValueError("Invalid email format. Please, write in format 'mail@mail.com'")
        super().__init__(email)
    
    def _email_check(self, email: str) -> bool:
        # Check correct email
        reg = r"[a-z]\w+@([a-z]{2,}\.)+[a-z]{2,}\b"
        email = re.search(reg, email)

        if not email:
            return True
        else:
            return False



class Birthday(Field):
    def __init__(self, date: str) -> None:
        self.correct_birthday = date

    @property
    def correct_birthday(self):
        return super().value

    @correct_birthday.setter
    def correct_birthday(self, date: str | object) -> None:
        date = str(date)
        date = self._birthday_check(date)
        if not date:
            raise ValueError("Invalid birthday format. Try firstly DAY, secondly MONTH, lastly YEARS")
        else:
            super().__init__(date)

    def __str__(self) -> str:
        if isinstance(self.value, datetime):
            return self.value.strftime("%d.%m.%Y")
        else:
            return self.value
        
    def _birthday_check(self,date: str) -> bool:
        splitters = [".", ",", "/", "-", ";", ":", "_"]
        for sign in splitters:
            date = date.replace(sign, " ")

        __match = re.match(r"\d{2} \d{2} \d{4}\b", date)
        if not __match:
            return False

        day, month, year = map(int, date.split())

        try:
            birthday = datetime(year, month, day)
            return birthday

        except:
            return False
        
    def days_to_birthday(self) -> int:
        today = datetime.today()
        next_birthday = datetime(today.year, self.value.month, self.value.day)
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, self.value.month, self.value.day)
        return (next_birthday - today).days
    


