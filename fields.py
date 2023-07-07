import re
from datetime import datetime


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    def __init__(self, name: str) -> None:
        self.correct_name = name

    @property
    def correct_name(self):
        return self.value

    @correct_name.setter
    def correct_name(self, value):
        if re.search(r"\W", value):
            raise ValueError(f"Invalid name format: {value}")
        super().__init__(value)


class Phone(Field):
    def __init__(self, number: str) -> None:
        self.correct_phone = number

    @property
    def correct_phone(self):
        return super().value

    @correct_phone.setter
    def correct_phone(self, value: str | object) -> None:
        value = str(value)
        check = phone_check(value)
        if not check:
            print((f"Invalid phone number format: {value}"))
        super().__init__(check)


class Email(Field):
    def __init__(self, email: str) -> None:
        self.correct_email = email

    @property
    def correct_email(self):
        return super().value

    @correct_email.setter
    def correct_email(self, email: str | object) -> None:
        email = str(email)
        if email_check(email):
            raise ValueError(f"Invalid email format: {email}")
        super().__init__(email)


class Birthday(Field):
    def __init__(self, date: str) -> None:
        self.correct_birthday = date

    @property
    def correct_birthday(self):
        return super().value

    @correct_birthday.setter
    def correct_birthday(self, date: str | object) -> None:
        date = str(date)
        # if date == "dd/mm/yyyy":
        #     super().__init__(date)
        #     return
        date = birthday_check(date)
        if not date:
            print(f"Invalid birthday format: {date}")
            return
        else:
            super().__init__(date)

    def __str__(self) -> str:
        if isinstance(self.value, datetime):
            return self.value.strftime("%d.%m.%Y")
        else:
            return self.value


def phone_check(phone_number):
    expected_length = 13

    # Check if phone number begin with +380
    if not phone_number.startswith("+380"):
        phone_number = "+380" + phone_number

    elif not phone_number.startswith("+38"):
        phone_number = "+38" + phone_number

    elif not phone_number.startswith("+3"):
        phone_number = "+3" + phone_number

    elif not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    # Check all symbols are numbers
    if not phone_number[1:].isdigit():
        print('Number is not digit')
        return False

    if len(phone_number) != expected_length:
        print('Length of number is not correct')
        return False

    return phone_number


def email_check(email: str) -> bool:
    # Check correct email
    reg = r"[a-z]\w+@([a-z]{2,}\.)+[a-z]{2,}\b"
    email = re.search(reg, email)

    if not email:
        return True
    else:
        return False


def birthday_check(date: str):
    splitters = [".", ",", "/", "-"]
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


def add_input_check(args: list) -> list | bool:
    if len(args) != 2:
        print(
            "INVALID INPUT: Not enough or too much charecters, to use this comand enter <name> <phone\mail> separated by space")
        return False
    return args


def invalid_show_input(args: list) -> str | bool:
    if len(args) > 1:
        print("INVALID INPUT: too much characters")
        return True

    try:
        value = args[0]
    except IndexError:
        print("INVALID INPUT: No name were written")
        return True

    return value
