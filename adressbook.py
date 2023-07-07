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


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
        print("Contact added successfully.")

    def search(self):
        # while True:
        # search values by keywords
        keyword = input('Input keyword: ')
        results = []
        for record in self.data.values():
            # convert to lower case to compare the entered keyword among values
            # add value to list if True
            if keyword.lower() in record.name.value.lower() or any(
                    keyword.lower() in phone.value.lower()[:len(keyword)] for phone in record.phones):
                results.append(record)

        if results:
            print("Search results:")
            for result in results:
                print(f"Name: {result.name.value}")
                for phone in result.phones:
                    print(f"Phone: {phone.value}")
                if result.birthday:
                    print(f"Birthday: {result.birthday.value.strftime('%Y-%m-%d')}")
            return results
        else:
            print("No results found.")


address_book = AddressBook()


def hello():
    return print("Hello! Enter command pls: ")


def exit_command():
    return print("Good bye!")


def new_contact():
    name = input("Enter the contact's name: ")
    phone = input("Enter the contact's phone number: ")
    email = input("Enter the contact's email: ")
    birthday = input("Enter the contact's birthday (YYYY-MM-DD-): ")
    return Record(Name(name), Phone(phone) if phone else None, Email(email) if email else None,
                  Birthday(datetime.strptime(birthday, '%Y-%m-%d')) if birthday else None)


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
    phone = input("Enter the new phone number: ")
    record = address_book.data.get(name)
    if record:
        if phone:
            new_phone = Phone(phone)
            record.edit_phone(record.phones[0], new_phone)
            print("Phone number updated successfully.")
        else:
            print("Invalid input. Please provide a new phone number.")
    else:
        print("No contact found with that name.")


def change_email():
    name = input("Enter the contact's name: ")
    email = input("Enter the new email: ")
    record = address_book.data.get(name)
    if record:
        if email:
            new_email = Email(email)
            record.edit_email(record.email[0], new_email)
            print("Email updated successfully.")
        else:
            print("Invalid input. Please provide a email.")
    else:
        print("No contact found with that name.")


def delete():
    deleted = input("Phone or User?").lower()
    if deleted.startswith("phone"):
        name = input("Enter the contact's name: ")
        phone = input("Enter the phone number to delete: ")
        record = address_book.data.get(name)
        phone_to_delete = Phone(phone)
        if phone_to_delete in record.phones:
            record.delete_phone(phone_to_delete)
            print("Phone number deleted successfully.")
        else:
            print("No matching phone number found.")

    elif deleted.startswith("user"):
        name = input("Enter the contact's name: ")
        record = address_book.data.get(name)
        if record:
            address_book.data.pop(name)
            print("Contact deleted successfully.")
        else:
            print("No contact found with that name.")


commands = {
    "hello": hello,
    "add phone": add_phone,
    "add mail": add_email,
    "add": add_contact,
    "change phone": change_phone,
    "change mail": change_email,
    "search": address_book.search,
    "delete": delete,
    "good bye": exit_command,
    "close": exit_command,
    "exit": exit_command,
}


def main(command):
    if command in commands:
        func = commands[command]
        func()
    else:
        print("Invalid command")


if __name__ == '__main__':
    while True:
        command = input("Enter a command: ").lower()
        main(command)