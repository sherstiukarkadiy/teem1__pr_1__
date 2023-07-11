from collections import UserDict
from .fields import *
from datetime import datetime
import sys


class Record:
    def __init__(self, name: Name = str, phone: Phone = None, email: Email = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.email = [] 
        self.birthday = birthday
        
        if phone:
            if isinstance(phone,list):
                self.phones.extend(phone)
            else:
                self.phones.append(phone)
        if email:
            if isinstance(email,list):
                self.email.extend(email)
            else:
                self.email.append(email)

    def add_phone(self, phone):
        self.phones.append(phone)

    def add_email(self, email):
        self.email.append(email)

    def delete_phone(self, phone):
        self.phones.remove(phone)
        
    def delete_birthday(self):
        self.birthday = None

    def delete_email(self, email):
        self.email.remove(email)
    
    def delete_birthday(self, birthday):
        self.phones.remove(birthday)

    def edit_phone(self, old_phone, new_phone):
        index_of_old_phone = self.phones.index(old_phone)
        self.phones[index_of_old_phone] = new_phone

    def edit_email(self, old_email, new_email):
        index_of_old_email = self.phones.index(old_email)
        self.email[index_of_old_email] = new_email
        
    def edit_birthday(self, birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            return (next_birthday - today).days

    def __repr__(self):
        line = "-" * 25
        name = self.name
        birth = str(self.birthday) or None
        phones = f"{', '.join(map(str, self.phones))}" or None
        emails = f"{', '.join(map(str, self.email))}" or None
        return f"{line}\nName: {name}\nPhones: {phones}\nEmailes: {emails}\nBirthday: {birth}\n{line}\n"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        if record.name.value in self.data:
            print("Contact with the same name already exists.")
            return
        self.data[record.name.value] = record
        print("Contact added successfully.")


def choose_from_menu(lst: list):
    menu_rows = []
    for ind,elem in enumerate(lst):
        menu_rows.append("{:^2}|{:^14}".format(ind+1,str(elem)))
    print("\n".join(menu_rows))
    
    while True:
        try:
            index = int(input("variant number: "))-1
            return lst[index]
        except ValueError as er:
            print(er)
            continue
        except IndexError as er:
            print(er)
            continue


def hello():
    return print("Hello! Enter command pls: ")


def new_contact():
    while True:
        try:
            name = input("Enter the contact's name: ")
            if not name:
                print("Can't create contact without name")
                return
            name = Name(name)
        except ValueError as e:
            print(str(e))
            continue
        break
    
    while True:
        try:
            phone = input("Enter the contact's phone number or pass: ")
            phone = Phone(phone) if phone else None
        except ValueError as e:
            print(str(e))
            continue
        break
        
    while True:
        try:
            email = input("Enter the contact's email (mail@mail.com) or pass: ")
            email = Email(email) if email else None
        except ValueError as e:
            print(str(e))
            continue
        break
    
    while True:
        try:
            birthday = input("Enter the contact's birthday (DD-MM-YYYY) or pass: ")
            birthday = Birthday(birthday) if birthday else None
        except ValueError as e:
            print(str(e))
            continue
        break

    return Record(name, phone, email, birthday)


def add_contact(address_book: AddressBook):
    record = new_contact()
    address_book.add_record(record)


def add_phone(address_book: AddressBook):
    name = input("Enter the contact's name: ")
    record = address_book.data.get(name)
    if record:
        try:
            phone = input("Enter the new phone number: ")
            if phone:
                new_phone = Phone(phone)
                record.add_phone(new_phone)
                print("Phone number added successfully.")
            else:
                print("No phone tiped")
        except ValueError as e:
            print(str(e))
    else:
        print("No contact found with that name. Add new contact\n")
        add_contact(address_book)


def add_email(address_book: AddressBook):
    name = input("Enter the contact's name: ")
    record = address_book.data.get(name)
    if record:
        try:
            email = input("Enter the new email: ")
            if email:
                new_email = Email(email)
                record.add_email(new_email)
                print("Email added successfully.")
            else:
                print("No email tiped")
        except ValueError as e:
            print(str(e))
    else:
        print("No contact found with that name. Add new contact\n")
        add_contact(address_book)

        
def add_birthday(address_book: AddressBook):
    name = input("Enter the contact's name: ")
    record = address_book.data.get(name)
    if record:
        try:
            birthday = input("Enter the new birthday: ")
            if birthday:
                new_birthday = Birthday(birthday)
                record.edit_birthday(new_birthday)
                print("Birthday added successfully.")
            else:
                print("No birthday tiped")
        except ValueError as e:
            print(str(e))
    else:
        print("No contact found with that name. Add new contact\n")
        add_contact(address_book)


def change_phone(address_book: AddressBook):
    name = input("Enter the contact's name: ")
    record = address_book.data.get(name)
    if record:
        if len(record.phones):
            print("Choose phone number you want to change:")
            old_phone = choose_from_menu(record.phones)
        else:
            old_phone = None
            
        try:
            phone = input("Enter the new phone: ")
            if phone and old_phone:
                new_phone = Phone(phone)
                record.edit_phone(old_phone, new_phone)
                print("Phome updated successfully.")
            elif phone and not old_phone:
                new_phone = Phone(phone)
                record.add_phone(old_phone, new_phone)
                print("Phone updated successfully.")
            else:
                print("No phone tiped")
        except ValueError as e:
            print(str(e))
    else:
        print("No contact found with that name.")


def change_email(address_book: AddressBook):
    name = input("Enter the contact's name: ")
    record = address_book.data.get(name)
    if record:
        if len(record.phones):
            print("Choose email you want to change:")
            old_email = choose_from_menu(record.email)
        else:
            old_email = None
       
        try:
            email = input("Enter the new email: ")
            if email and old_email:
                new_email = Email(email)
                record.edit_email(old_email, new_email)
                print("Email updated successfully.")
            elif email and not old_email:
                new_email = Email(email)
                record.add_email(old_email, new_email)
                print("Email updated successfully.")
            else:
                print("No email tiped")
        except ValueError as e:
            print(str(e))
    else:
        print("No contact found with that name.")


def day_birthday(address_book: AddressBook):
    name = input("Enter the contact's name: ")
    record = address_book.data.get(name)
    if record:
        day = record.days_to_birthday()
        print(day)


def delete(address_book: AddressBook):
    deleted = input("Phone, Email, Birthday or User? ").lower()
    name = input("Enter the contact's name: ")
    record = address_book.data.get(name)
    
    if deleted.strip().startswith("phone"):
        
        if record and len(record.phones):
            print("Choose phone number you want to delete:")
            phone_to_delete = choose_from_menu(record.phones)
        elif record and not len(record.phones):
            phone_to_delete = None
        else:
            print("No contact found with that name.")
            
        if phone_to_delete:
            record.delete_phone(phone_to_delete)
            print("Phone number deleted successfully.")
        else:
            print("Contact don't have any numbers.")

    elif deleted.strip().startswith("mail"):
        
        if record and len(record.email):
            print("Choose email you want to delete:")
            email_to_delete = choose_from_menu(record.email)
        elif record and not len(record.email):
            email_to_delete = None
        else:
            print("No contact found with that name.")
            
        if email_to_delete:
            record.delete_email(email_to_delete)
            print("Email deleted successfully.")
        else:
            print("Contact don't have any emailes.")
            
    elif deleted.strip().startswith("birthday"):
        
        if record and len(record.birthday):
            record.delete_birthday()
            print("Birtday deleted successfully.")
        elif record and not len(record.email):
            print("Contact don't have any emailes.")
        else:
            print("No contact found with that name.")

    elif deleted.strip().startswith("user"):
        
        if record:
            address_book.data.pop(name)
            print("Contact deleted successfully.")
        else:
            print("No contact found with that name.")


def search_contacts(address_book: AddressBook):
    keyword = input('Input keyword: ')
    results = []
    for record in address_book.data.values():
        record_str = str(record).replace("Name:","")
        record_str = record_str.replace("Phones:","")
        record_str = record_str.replace("Emailes:","")
        record_str = record_str.replace("Birthday:","")
        if keyword.lower() in record_str.lower():
            results.append(record)

    if results:
        print("Search results:")
        for result in results:
            print(result)
    else:
        print("No results found.")
        
def show_all_contacts(address_book: AddressBook):
    for record in address_book.values():
        print(str(record) + "\n")
        
def close(*args) -> None:
        """breake all program
        """
        
        print("Good bye")
        sys.exit()
