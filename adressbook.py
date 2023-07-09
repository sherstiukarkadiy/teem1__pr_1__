from collections import UserDict
from fields import *
from datetime import datetime


class Record:
    def __init__(self, name: Name = str, phone: Phone = None, email: Email = None, birthday: Birthday = None):
        self.name = name
        self.phones = [] if phone is None else [phone]
        self.email = [] if email is None else [email]
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def add_email(self, email):
        self.email.append(email)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def delete_email(self, email):
        self.email.remove(email)

    def edit_phone(self, old_phone, new_phone):
        index_of_old_phone = self.phones.index(old_phone)
        self.phones[index_of_old_phone] = new_phone

    def edit_email(self, old_email, new_email):
        index_of_old_email = self.phones.index(old_email)
        self.email[index_of_old_email] = new_email

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            return (next_birthday - today).days

    def __repr__(self):
        name = self.name
        birth = str(self.birthday) or None
        phones = f"{', '.join(map(str, self.phones))}" or None
        emails = f"{', '.join(map(str, self.email))}" or None
        return f"Name: {name}\nPhones: {phones}\nEmails: {emails}\nBirthday: {birth}"


class AddressBook(UserDict):

    def add_record(self, record):
        if record.name.value in self.data:
            print("Contact with the same name already exists.")
            return
        self.data[record.name.value] = record
        print("Contact added successfully.")


address_book = AddressBook()


def hello():
    return print("Hello! Enter command pls: ")


def new_contact():
    # while True:
    #     try:
    name = input("Enter the contact's name: ")
    phone = input("Enter the contact's phone number: ")
    email = input("Enter the contact's email (mail@mail.com): ")
    birthday = input("Enter the contact's birthday (DD-MM-YYYY): ")

    return Record(Name(name), Phone(phone) if phone else None, Email(email) if email else None,
                  Birthday(birthday) if birthday else None)


def add_contact():
    record = new_contact()
    address_book.add_record(record)


def add_phone():
    name = input("Enter the contact's name: ")
    phone = input("Enter the new phone number: ")
    record = address_book.data.get(name)
    if record:
        if phone:
            new_phone = Phone(phone)
            record.add_phone(new_phone)
            print("Phone number added successfully.")
        else:
            print("Invalid input. Please provide a new phone number.")
    else:
        print("No contact found with that name.")


def add_email():
    name = input("Enter the contact's name: ")
    email = input("Enter the new email: ")
    record = address_book.data.get(name)
    if record:
        if email:
            new_email = Email(email)
            record.add_email(new_email)
            print("Email added successfully.")
        else:
            print("Invalid input. Please provide a new email.")
    else:
        print("No contact found with that name.")


def change_phone():
    name = input("Enter the contact's name: ")
    old_phone = input("Enter the old phone: ")
    phone = input("Enter the new phone number: ")
    record = address_book.data.get(name)
    if record:
        if phone:
            new_phone = Phone(phone)
            record.edit_phone(old_phone, new_phone)
            print("Phone number updated successfully.")
        else:
            print("Invalid input. Please provide a new phone number.")
    else:
        print("No contact found with that name.")


def change_email():
    name = input("Enter the contact's name: ")
    old_email = input("Enter the old email: ")
    email = input("Enter the new email: ")
    record = address_book.data.get(name)
    if record:
        if email:
            new_email = Email(email)
            record.edit_email(old_email, new_email)
            print("Email updated successfully.")
        else:
            print("Invalid input. Please provide a email.")
    else:
        print("No contact found with that name.")


def day_birthday():
    name = input("Enter the contact's name: ")
    record = address_book.data.get(name)
    if record:
        day = record.days_to_birthday()
        print(day)


def delete():
    deleted = input("Phone, Email or User? ").lower()
    if deleted.strip().startswith("phone"):
        name = input("Enter the contact's name: ")
        phone = input("Enter the phone number to delete: ")
        record = address_book.data.get(name)
        phone_to_delete = Phone(phone)
        if phone_to_delete in record.phones:
            record.delete_phone(phone_to_delete)
            print("Phone number deleted successfully.")
        else:
            print("No matching phone number found.")

    if deleted.strip().startswith("mail"):
        name = input("Enter the contact's name: ")
        email = input("Enter the email to delete: ")
        record = address_book.data.get(name)
        email_to_delete = Email(email)
        if email_to_delete in record.email:
            record.delete_email(email_to_delete)
            print("Email deleted successfully.")
        else:
            print("No matching email found.")

    elif deleted.strip().startswith("user"):
        name = input("Enter the contact's name: ")
        record = address_book.data.get(name)
        if record:
            address_book.data.pop(name)
            print("Contact deleted successfully.")
        else:
            print("No contact found with that name.")


def search_contacts():
    keyword = input('Input keyword: ')
    results = []
    for record in address_book.data.values():
        if keyword.lower() in record.name.value.lower():
            results.append(record)

    if results:
        print("Search results:")
        for result in results:
            print(result)
    else:
        print("No results found.")


commands = {
    "hello": hello,
    "add phone": add_phone,
    "add mail": add_email,
    "add": add_contact,
    "change phone": change_phone,
    "change mail": change_email,
    "search": search_contacts,
    "birthday": day_birthday,
    "delete": delete
}


def main():
    while True:
        command = input("Enter a command: ").lower()
        if command in commands:
            func = commands[command]
            func()
        elif command.strip().startswith("good bye") or command.strip().startswith(
                "close") or command.strip().startswith("exit"):
            print("Good bye!")
            break
        else:
            print("Invalid command")


if __name__ == '__main__':
    main()
