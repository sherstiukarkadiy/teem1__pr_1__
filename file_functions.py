import csv
import json
from adressbook import *
from fields import *
from notes import *

def save_data_to_files(addressbook, notes, adressbook_path, notes_path):
    save_addressbook_to_csv(adressbook_path, addressbook)
    save_notes_to_json(notes_path, notes)
    print("Data saved to files.")

def load_data_from_files(adressbook_path, notes_path):
    addressbook = load_contacts_from_csv(adressbook_path)
    notes = load_notes_from_json(notes_path)
    return addressbook, notes

def save_addressbook_to_csv(file_path, addressbook: AddressBook):
    # Знаходимо максимальну кількість номерів телефону та адрес електронної пошти серед усіх контактів
    
    if not dict(addressbook):
        return
    
    max_phone_count = max([len(record.phones) for record in addressbook.values()])
    max_email_count = max([len(record.email) for record in addressbook.values()])

    # Створюємо заголовки для номерів телефону та адрес електронної пошти
    phone_headers = [f"Phone {i+1}" for i in range(max_phone_count)]
    email_headers = [f"Email {i+1}" for i in range(max_email_count)]

    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        headers = ["Name", "Birthday"] + phone_headers + email_headers
        writer.writerow(headers)

        for record in addressbook.values():
            # Заповнюємо порожні місця в номерах телефону та адресах електронної пошти
            phone_numbers = record.phones + [""] * (max_phone_count - len(record.phones))
            email_addresses = record.email + [""] * (max_email_count - len(record.email))

            writer.writerow([str(record.name), record.birthday] + [str(phone) if phone else "N/A" for phone in phone_numbers] + [str(email) if email else "N/A" for email in email_addresses])

    print("Address book saved to CSV:", file_path)

def load_contacts_from_csv(file_path):
    addressbook = AddressBook()
    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        try:
            header = next(reader)
        except:
            return addressbook
        
        phone_indices = [i for i, col in enumerate(header) if "Phone" in col]
        email_indices = [i for i, col in enumerate(header) if "Email" in col]
        
        for row in reader:
            name = Name(row[0])
            birthday = Birthday(row[1]) if row[1] else None
            phone_numbers = [row[i] for i in phone_indices if i < len(row) and row[i] != "N/A"]
            email_addresses = [row[i] for i in email_indices if i < len(row) and row[i] != "N/A"]
            addressbook.add_record(Record(name, phone=phone_numbers, email=email_addresses, birthday=birthday))
    return addressbook

def save_notes_to_json(file_path, notes):
    if not dict(notes):
        return
    with open(file_path, "w") as json_file:
        json.dump(dict(notes), json_file, indent=4)
    print("Notes saved to JSON:", file_path)
    
def load_notes_from_json(file_path):
    with open(file_path, "r") as json_file:
        try:
            notes = json.load(json_file)
        except:
            notes = Notebook()
    return Notebook(notes)

