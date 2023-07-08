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
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "Phone", "Email"])
        for record in addressbook:
            writer.writerow([str(record.name), record.phone, record.email])
    print("Address book saved to CSV:", file_path)

def load_contacts_from_csv(file_path):
    addressbook = AddressBook()
    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            name = Name(row[0])
            birthday = Birthday(row[1])
            phone_numbers = [num for num in row[2:6] if num != "-"]
            email_addresses = [email for email in row[6:8] if email != "-"]
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
