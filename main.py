from adressbook import *
from notes import *
from file_functions import *
from files_sorting import main_sorting
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

CONTACTS_PATH = Path(__file__).parent.joinpath("Contacts.csv")
NOTES_PATH = Path(__file__).parent.joinpath("Notes.json")
with open(CONTACTS_PATH,"w") as f:
    pass
with open(NOTES_PATH,"w") as f:
    pass
contacts,notebook = load_data_from_files(CONTACTS_PATH, NOTES_PATH)

logic_commands = {
    "hello": hello,
    "good bye": close,
    "close": close,
    "exit": close,
    "sort folder": main_sorting
}

contacts_commands = {
    "add phone": add_phone,
    "add mail": add_email,
    "add contact": add_contact,
    "change phone": change_phone,
    "change mail": change_email,
    "search contact": search_contacts,
    "birthday": day_birthday,
    "delete": delete,
}

note_comands = {
    "add note": add_note,
    "search note": search_note,
    "delete note": delete_note,
    "edit note": edit_note,
    "show notes": show_all_notes
}

word_completer = WordCompleter([i for i in logic_commands]+[j for j in contacts_commands]+[n for n in note_comands])

def main_func():
    try:
        while True:
            command = prompt("Enter a command: ",completer=word_completer).strip().lower()
            if command in logic_commands:
                func = logic_commands[command]
                func()
            elif command in contacts_commands:
                func = contacts_commands[command]
                func(contacts)
            elif command in note_comands:
                func = note_comands[command]
                func(notebook)
            elif command == "help":
                line = "-" * 22
                head_1 = "|{:^20}|".format("logic commands")
                head_2 = "|{:^20}|".format("contacts commands")
                head_3 = "|{:^20}|".format("notes commands")
                
                body_1 = ["|{:^20}|".format(i) for i in logic_commands]
                body_2 = ["|{:^20}|".format(i) for i in contacts_commands]
                body_3 = ["|{:^20}|".format(i) for i in note_comands]
                
                output_list = [line,head_1,line] + body_1 + ["\n"+line,head_2,line] + body_2 + ["\n"+line,head_3,line] + body_3
                print("\n".join(output_list))
            else:
                print("Invalid command")
    finally:
        save_data_to_files(contacts,notebook,CONTACTS_PATH,NOTES_PATH)
        
main_func()