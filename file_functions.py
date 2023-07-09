import csv
import json

def save_data_to_files(addressbook, notes):
    save_addressbook_to_csv("Contacts.csv", addressbook)
    save_notes_to_json("Notes.json", notes)
    print("Data saved to files.")

def load_data_from_files():
    addressbook = load_contacts_from_csv("Contacts.csv")
    notes = load_notes_from_json("Notes.json")
    print("Data loaded from files.")
    return addressbook, notes

def save_addressbook_to_csv(file_path, addressbook):
    # Знаходимо максимальну кількість номерів телефону та адрес електронної пошти серед усіх контактів
    max_phone_count = max([len(record.phone) for record in addressbook])
    max_email_count = max([len(record.email) for record in addressbook])

    # Створюємо заголовки для номерів телефону та адрес електронної пошти
    phone_headers = [f"Phone {i+1}" for i in range(max_phone_count)]
    email_headers = [f"Email {i+1}" for i in range(max_email_count)]

    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        headers = ["Name", "Birthday"] + phone_headers + email_headers
        writer.writerow(headers)

        for record in addressbook:
            # Заповнюємо порожні місця в номерах телефону та адресах електронної пошти
            phone_numbers = record.phone + [""] * (max_phone_count - len(record.phone))
            email_addresses = record.email + [""] * (max_email_count - len(record.email))

            writer.writerow([str(record.name), record.birthday] + phone_numbers + email_addresses)

    print("Address book saved to CSV:", file_path)

def load_contacts_from_csv(file_path):
    addressbook = AddressBook()
    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        
        phone_indices = [i for i, col in enumerate(header) if "Phone" in col]
        email_indices = [i for i, col in enumerate(header) if "Email" in col]
        
        for row in reader:
            name = Name(row[0])
            birthday = Birthday(row[1])
            phone_numbers = [row[i] for i in phone_indices if i < len(row) and row[i] != ""]
            email_addresses = [row[i] for i in email_indices if i < len(row) and row[i] != ""]
            addressbook.add_record(Record(name, phone=phone_numbers, email=email_addresses, birthday=birthday))
    return addressbook

def save_notes_to_json(file_path, notes):
    with open(file_path, "w") as json_file:
        json.dump(notes, json_file, indent=4)
    print("Notes saved to JSON:", file_path)

def load_notes_from_json(file_path):
    with open(file_path, "r") as json_file:
        notes = json.load(json_file)
    return notes
