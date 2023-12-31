from collections import UserDict
from datetime import datetime

class Notebook(UserDict):
    note_id = 1000
    def __init__(self,dictionary = None):
        self.data = {} if not dictionary else dictionary
    
    def add(self, note):
        last_id = max(self.data.keys()) if self.data else 1000
        self.note_id = int(last_id) + 1
        self.note_id = str(self.note_id)
        record = {'Title' : note.title,
                  'Text' : note.body, 
                  'Tags' : note.tags,
                  'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')}
        self.data[self.note_id] = record

    def __str__(self):
        result = []
        for note_id, record in sorted(self.data.items(), key=lambda x: x[0]):
            result.append(
                "_" * 50 + "\n" + f"ID: {note_id} \nTitle: {record['Title']} \nText:\n {record['Text']} \nTags: {record['Tags']} \nCreation time: {record['Timestamp']} \n" + "_" * 50 + '\n')
        return '\n'.join(result)

    def search(self, pattern, category):
        result = []
        category_new = category.strip().lower()
        pattern_new = pattern.strip().lower()

        for note_id, record in self.data.items():
            if category_new == '1': # Поиск по названию заметки
                if record['Title'].lower().startswith(pattern_new):
                    result.append(
                        "_" * 50 + "\n" + f"Title: {record['Title']} \nText:\n {record['Text']} \nTags: {record['Tags']} \nCreation time: {record['Timestamp']} \n" + "_" * 50)
            elif category_new == '2': # Поиск совпадений в тексте
                if pattern_new in record["Text"]:
                    result.append(
                        "_" * 50 + "\n" + f"Title: {record['Title']} \nText:\n {record['Text']} \nTags: {record['Tags']} \nCreation time: {record['Timestamp']} \n" + "_" * 50)
            elif category_new == '3': # Поиск по тегам
                if pattern_new in [tag.lower().replace(' ', '') for tag in record.get('Tags', [])]:
                    result.append(
                        "_" * 50 + "\n" + f"ID: {note_id} \nTitle: {record['Title']} \nText:\n {record['Text']} \nTags: {record['Tags']} \nCreation time: {record['Timestamp']} \n" + "_" * 50)   
        if not result:
            print('There is no such note in notebook')
        return 'Here is what we found for your request:\n' + '\n'.join(result)
    
    def sort_notes(self, field):
        result = []
        
        if field == '1':
            result = 'Here is what we found for your request:\n' + str(self)
            return result
        elif field == '2':
            for note_id, record in sorted(self.data.items(), key=lambda x: x[1]["Title"]):
                result.append(
                    "_" * 50 + "\n" + f"ID: {note_id} \nTitle: {record['Title']} \nText:\n {record['Text']} \nTags: {record['Tags']} \nCreation time: {record['Timestamp']} \n" + "_" * 50 + '\n')
            return 'Here is what we found for your request:\n' + '\n'.join(result)
        elif field == '3':
            tag = input("Please enter a tag to sort by: ")
            for note_id, record in sorted(self.data.items(), key=lambda x: x[0]):
                if tag.lower() in [t.lower() for t in record.get('Tags', [])]:
                    result.append(
                        "_" * 50 + "\n" + f"ID: {note_id} \nTitle: {record['Title']} \nText:\n {record['Text']} \nTags: {record['Tags']} \nCreation time: {record['Timestamp']} \n" + "_" * 50)
            for note_id, record in sorted(self.data.items(), key=lambda x: x[0]):
                if tag.lower() not in [t.lower() for t in record.get('Tags', [])]:
                    result.append(
                        "_" * 50 + "\n" + f"ID: {note_id} \nTitle: {record['Title']} \nText:\n {record['Text']} \nTags: {record['Tags']} \nCreation time: {record['Timestamp']} \n" + "_" * 50)
            return 'Here is what we found for your request:\n' + '\n'.join(result)
        else:
            print(f"Invalid field '{field}'.")
            
    

    def delete(self, title):
        for note_id, record in self.data.items():
            if record['Title'].lower() == title.lower():
                del self.data[note_id]
                print(f"Note with title '{title}' deleted from notebook.")
                return
        else:
            print(f"Note with title '{title}' does not exist in the notebook.")

    def edit(self, title, field, new_value):
        for record in self.data.values():
            if title in record['Title']:
                if field == '1':
                    record['Title'] = new_value
                elif field == '2':
                    record['Text'] = new_value
                elif field == '3':
                    record['Tags'] = [tag.strip() for tag in new_value.split(',')] 
                else:
                    print(f"Invalid field '{field}'.")
        else:
            print(f"Note with Title {title} does not exist in the notebook.")

class Note:
    def __init__(self, title, body, tags):
        self.title = title
        self.body = body
        self.tags = [tag.strip() for tag in tags.split(',')]

class Title(Note):
    def __init__(self, value):
        self.value = value

class Body(Note):
    def __init__(self, value):
        self.value = value

class Tags(Note):
    def __init__(self, value):
        self.value = value

def add_note(notebook: Notebook): 
    """Добавление новой заметки"""
    
    title = Title(input('Please write a title: ')).value.strip()
    print('Write your note: ', end="")
    body = Body("\n".join(iter(input, ""))).value
    tags = Tags(input('Add tags to your note: ')).value
    note = Note(title, body, tags)
    return notebook.add(note)

def search_note(notebook: Notebook):  
    """Поиск по заметкам"""
    
    print("There are following categories: \n1 | Title \n2 | Text \n3 | Tags")
    category = input('Search number of category: ')
    pattern = input('Search pattern: ')
    result = (notebook.search(pattern, category))
    print(result)
    
def delete_note(notebook: Notebook):
    """Удаление заметки по её названию"""
    
    pattern = input('Please enter a Title of note you want to delete: ')
    notebook.delete(pattern)
    
def edit_note(notebook: Notebook):
    """Редактироваие заметок"""
    
    title = input("Please enter a Title of note you want to edit: ")
    print("You can edit following fields: \n1 | Title \n2 | Text \n3 | Tags")
    field = input('Enter a field number: ')
    new_value = input('Enter new value: ')
    notebook.edit(title, field, new_value)
    print("The note has been changed.")
    
def sort_notes(notebook: Notebook):
    print("You can sort by following fields: \n1 | ID \n2 | Title \n3 | Tags")
    field = input('Enter a field number: ')
    result = notebook.sort_notes(field)
    print(result)
    
def show_all_notes(notebook: Notebook):
    """Вывод всего списка заметок"""
    
    print(notebook)


# if __name__ == "__main__":
#     print('Hello. I am your notebook \nChoose the required command: \n1 | Add \n2 | Search \n3 | Delete \n4 | Edit \n5 | View \n6 | Exit')
#     handler = Handler()
#     commands = ['Add','View', 'Search', 'Edit', 'Delete', 'Exit']
#     while True:
#         action = input('Choose a number: ').strip()
#         handler.handle(action)
#         if action == '6':
#             print('Good bye!')
#             break
#         print('Choose the required command: \n1 | Add \n2 | Search \n3 | Delete \n4 | Edit \n5 | View \n6 | Exit')

