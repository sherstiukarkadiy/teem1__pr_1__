from collections import UserDict
from datetime import datetime, date

class Notebook(UserDict):
    def __init__(self):
        self.data = {}
    
    def add(self, note):
        note_id = ID()
        record = {'Title' : note.title,
                  'Text' : note.body, 
                  'Tags' : note.tags}
        self.data[note_id] = record

    def __str__(self):
        result = []
        for note_id, record in self.data.items():
            result.append("_" * 50 + "\n" + f"ID: {note_id} \nTitle: {record['Title']} \nText: {record['Text']} \nTags: {record['Tags']} \n" + "_" * 50 + '\n')
        return '\n'.join(result)

    def search(self, pattern, category):
        result = []
        category_new = category.strip().lower().replace(' ', '')
        pattern_new = pattern.strip().lower().replace(' ', '')

        for note_id, record in self.data.items():
            if category_new == 'title':
                if record['Title'].lower().startswith(pattern_new):
                    result.append("_" * 50 + "\n" + f"Title: {record['Title']} \nText: {record['Text']} \nTags: {record['Tags']} \n" + "_" * 50 + '\n')
                elif record.get(category_new, '').lower().replace(' ', '') == pattern_new:
                    result.append(
                        "_" * 50 + "\n" + f"Title: {record['Title']} \nText: {record['Text']} \nTags: {record['Tags']} \n" + "_" * 50 + '\n')
            if category_new == 'tags':
                if record['Tags'].lower().startswith(pattern_new):
                    result.append(
                        "_" * 50 + "\n" + f"Title: {record['Title']} \nText: {record['Text']} \nTags: {record['Tags']} \n" + "_" * 50 + '\n')
                elif record.get(category_new, '').lower().replace(' ', '') == pattern_new:
                    result.append(
                        "_" * 50 + "\n" + f"Title: {record['Title']} \nText: {record['Text']} \nTags: {record['Tags']} \n" + "_" * 50 + '\n')
            if category_new == 'text':
                if record['Text'].lower().startswith(pattern_new):
                    result.append(
                        "_" * 50 + "\n" + f"Title: {record['Title']} \nText: {record['Text']} \nTags: {record['Tags']} \n" + "_" * 50 + '\n')
                elif record.get(category_new, '').lower().replace(' ', '') == pattern_new:
                    result.append(
                        "_" * 50 + "\n" + f"Title: {record['Title']} \nText: {record['Text']} \nTags: {record['Tags']} \n" + "_" * 50 + '\n')
        if not result:
            print('There is no such note in notebook')
        return '\n'.join(result)

    def delete(self, title):
        for note_id, record in self.data.items():
            if record['Title'].lower() == title.lower():
                del self.data[note_id]
                print(f"Note with title '{title}' deleted from notebook.")
                return
            else:
                print(f"Note with title '{title}' does not exist in the notebook.")

    def edit(self, title, field, new_value):
        for note_id, record in self.data.items():
            if title in record['Title']:
                if field.lower() == 'title':
                    record['Title'] = new_value
                elif field.lower() == 'text':
                    record['Text'] = new_value
                elif field.lower() == 'tags':
                    record['Tags'] = new_value
                else:
                    print(f"Invalid field '{field}'.")
            else:
                print(f"Note with Title {title} does not exist in the notebook.")

class Note:
    def __init__(self, title, body, tags = None):
        self.title = title
        self.body = body
        if tags is not None:
            self.tags = tags
        else:
            self.tags = None

class ID:
    note_id = 10000 
    def __init__(self):
        self.value = ID.note_id
        ID.note_id += 1

    def __str__(self):
        return str(self.value)

class Title(Note):
    def __init__(self, value):
        self.value = value

class Body(Note):
    def __init__(self, value):
        self.value = value

class Tags(Note):
    def __init__(self, value):
        self.value = value

class Publication:
    pass

class Handler:
    def __init__(self):
        self.notebook = Notebook()

    def handle(self, action):
        if action == 'add':
            title = Title(input('Please write a title: ')).value.strip()
            body = Body(input('Write your note: ')).value
            tags = Tags(input('Add tags to your note: ')).value
            note = Note(title, body, tags)
            return self.notebook.add(note)
        elif action == 'search':
            print("There are following categories: \nTitle \nText \nTags")
            category = input('Search category: ')
            pattern = input('Search pattern: ')
            result = (self.notebook.search(pattern, category))
            print(result)
        elif action == 'delete':
            pattern = input('Please enter a Title of note you want to delete: ')
            self.notebook.delete(pattern)
        elif action == 'edit':
            title = input("Please enter a Title of note you want to edit: ")
            print("You can edit following fields: \nTitle \nText \nTags")
            field = input('Enter a field: ')
            new_value = input('Enter new value: ')
            self.notebook.edit(title, field, new_value)
            print("The note has been changed.")
        elif action == 'view':
            print(self.notebook)
        elif action == 'exit':
            pass


if __name__ == "__main__":
    print('Hello. I am your notebook')
    handler = Handler()
    commands = ['Add','View', 'Exit', 'Search']
    while True:
        action = input(
            'Type help for list of commands or enter your command\n').strip().lower()
        if action == 'help':
            format_str = str('{:%s%d}' % ('^', 20))
            for command in commands:
                print(format_str.format(command))
            action = input().strip().lower()
            handler.handle(action)
        else:
            handler.handle(action)
        if action == 'exit':
            break
