from abc import ABC,abstractmethod
from collections import UserDict,UserList
from datetime import datetime
from enum import Enum
import json
from typing import Any,Dict

class NoteFieldNames(str, Enum):
    Id = "id"
    Title = "title"
    Body = "body"
    Tags = "tags"
    Time = "timestamp"
     

#NOTES CLASSES-----------------------------------  
class NoteField(ABC):
    @abstractmethod
    def __repr__ (self):
        pass
    
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value
    
    def __lt__(self, __value: object) -> bool:
        return self.value < __value.value
    
    def __le__(self, __value: object) -> bool:
        return self.value <= __value.value
    
    def __ne__(self, __value: object) -> bool:
        return self.value != __value.value
    
    def __ge__(self, __value: object) -> bool:
        return self.value >= __value.value
    
    def __gt__(self, __value: object) -> bool:
        return self.value > __value.value
    
class NoteId(NoteField):
    def __init__(self, value: str):
        self.value = value
    
    def __repr__ (self) -> str:
        return f"ID: {self.value}"
    
    def __int__(self) -> int:
        return self.value

class Title(NoteField):
    def __init__(self, value: str):
        self.value = value
    
    def __repr__ (self) -> str:
        return f"Title: {self.value}"

class Body(NoteField):
    def __init__(self, value: str):
        self.value = value
        
    def __repr__ (self) -> str:
        return f"Body: {self.value}"

class Tags(NoteField):
    def __init__(self, value: list[str]):
        self.value = value
        
    def __repr__ (self) -> str:
        return f"Tags: " + ";".join(self.value)

        
class CreationTime(NoteField):
    def __init__(self, value: str):
        self.value = value
        
    def __repr__(self) -> str:
        return "Creation time: " + self.value
    
class Note(UserDict):
    def __init__(self, note_id: NoteField, title: NoteField, body: NoteField, tags: NoteField, timestamp: NoteField) -> None:
        self.data = {
                NoteFieldNames.Id: note_id,
                NoteFieldNames.Title: title,
                NoteFieldNames.Body: body,
                NoteFieldNames.Tags: tags,
                NoteFieldNames.Time: timestamp
            }
    
    def __repr__(self) -> str:
        note_card = ("_" * 50 + "\n" + 
        f"""{self.data[NoteFieldNames.Id]}
        \r{self.data[NoteFieldNames.Title]} 
        \r{self.data[NoteFieldNames.Body]} 
        \r{self.data[NoteFieldNames.Tags]} 
        \r{self.data[NoteFieldNames.Time]}\n""" + 
        "_" * 50 + '\n')
        return note_card
    
    def __eq__(self, __other: object) -> bool:
        return dict(self.data) == dict(__other)
    
    def to_dict(self):
        return {ind:value.value for ind,value in self.data.items()}


#SEARCHING CLASSES-----------------------------------  
class Searcher(ABC):
    def __init__(self, data: list[Note]) -> None:
        self.data = data
    
    @abstractmethod
    def find_all(self):
        pass

class IdSearcher(Searcher):
    def find_all(self, pattern: str) -> list[Note]:
        for record in self.data:
            if record[NoteFieldNames.Id].value == pattern:
                return [record]
        else:
            return []
            
class TitleSearcher(Searcher):
    def find_all(self, pattern: str) -> list[Note]:
        matches = []
        for record in self.data:
            if pattern.lower() in record[NoteFieldNames.Title].value.lower() :
                matches.append(record)
        
        return matches

class BodySearcher(Searcher):
    def find_all(self, pattern: str) -> list[Note]:
        matches = []
        for record in self.data:
            if pattern.lower() in record[NoteFieldNames.Body].value.lower() :
                matches.append(record)
        
        return matches
class TagSearcher(Searcher):
    def find_all(self, pattern: str) -> list[Note]:
        matches = []
        for record in self.data:
            if pattern in record[NoteFieldNames.Tags].value:
                matches.append(record)
        
        return matches

class TimeSearcher(Searcher):
    def find_all(self, pattern: str) -> list[Note]|None:
        matches = []
        for record in self.data:
            if pattern.lower() in record[NoteFieldNames.Time].value.lower() :
                matches.append(record)
        
        return matches


#SORTING CLASSES-----------------------------------  
class Sorter(ABC):
    def __init__(self, data: list[Note]) -> None:
        self.data = data
    
    @abstractmethod
    def sort(self):
        pass

class IdSorter(Sorter):
    def sort(self,reverse:bool = False) -> list[Note]:
        return sorted(self.data, key=lambda x: x[NoteFieldNames.Id],reverse=reverse)
            
class TitleSorter(Sorter):
    def sort(self,reverse:bool = False) -> list[Note]:
        return sorted(self.data, key=lambda x: x[NoteFieldNames.Title],reverse=reverse)

class BodySorter(Sorter):
    def sort(self,reverse:bool = False) -> list[Note]:
        return sorted(self.data, key=lambda x: x[NoteFieldNames.Body],reverse=reverse)

class TagSorter(Sorter):
    def sort(self, reverse:bool = False) -> list[Note]:
        return sorted(self.data, key=lambda x: sorted(x[NoteFieldNames.Tags].value),reverse=reverse)
    
class TimeSorter(Sorter):
    def sort(self,reverse:bool = False) -> list[Note]:
        return sorted(self.data, key=lambda x: datetime.strptime(x[NoteFieldNames.Time],"%Y-%m-%d %H:%M"),reverse=reverse)

#NOTES OPERATION CLASSES-----------------------------------        
class NoteOperation(ABC):
    
    @abstractmethod
    def realize(self):
        pass

class NoteCreator(NoteOperation):
    note_id = 0
    
    def __init__(self, note:Dict[str, Any]) -> None:
        NoteCreator.note_id += 1
        
        self.id = note.get(NoteFieldNames.Id) or self.note_id
        self.title = note.get(NoteFieldNames.Title)
        self.body = note.get(NoteFieldNames.Body)
        self.tags = note.get(NoteFieldNames.Tags)
        self.timestamp = note.get(NoteFieldNames.Time) or datetime.now().strftime('%Y-%m-%d %H:%M')
    
    def realize(self) -> Note:
        self._tags_creator()
        self.note = Note(NoteId(self.id),Title(self.title),Body(self.body),Tags(self.tags),CreationTime(self.timestamp))
        return self.note
    
    def _tags_creator(self) -> None:
        if not isinstance(self.tags, list) and self.tags:
            self.tags = [tag.strip() for tag in self.tags.split(",")]
        elif not self.tags:
            self.tags = []
        
class NoteSearcher(NoteOperation):
    search_fields = {
        NoteFieldNames.Id: IdSearcher,
        NoteFieldNames.Title: TitleSearcher,
        NoteFieldNames.Body: BodySearcher,
        NoteFieldNames.Tags: TagSearcher,
        NoteFieldNames.Time: TimeSearcher
    }
    
    def __init__(self, data:list[Note]) -> None:
        self.data = data
        
    def realize(self,field: str,pattern: str) -> list[Note]:
        if not field.lower() in self.search_fields:
            return []

        searcher = self.search_fields.get(field.lower())(self.data)
        return searcher.find_all(pattern)
    
class NoteSorter(NoteOperation):
    sorting_fields = {
        NoteFieldNames.Id: IdSorter,
        NoteFieldNames.Title: TitleSorter,
        NoteFieldNames.Body: BodySorter,
        NoteFieldNames.Tags: TagSorter,
        NoteFieldNames.Time: TimeSorter
    }
    
    def __init__(self, data:list[Note]) -> None:
        self.data = data
        
    def realize(self,field:str, reverse:bool = False) -> list[Note]:
        if not field.lower() in self.sorting_fields:
            return []

        sorter = self.sorting_fields.get(field.lower())(self.data)
        return sorter.sort(reverse)

class NoteInRangeFounder(NoteOperation):
    
    def __init__(self, data:list[Note]) -> None:
        self.data = data
    
    def realize(self, _from: datetime ,_to: datetime) -> list[Note]:        
        _from = datetime.min if not _from else _from
        _to = datetime.max if not _to else _to
        
        result = []
        for note in self.data:
            if _from <= note[NoteFieldNames.Time] <= _to:
                result.append(note)
        
        return result
    
class NoteEditor(NoteOperation):
    def __init__(self,old_note: Note, new_note:Dict[str, Any]) -> None:

        self.id = old_note.get(NoteFieldNames.Id)
        self.title = new_note.get(NoteFieldNames.Title) or old_note.get(NoteFieldNames.Title).value
        self.body = new_note.get(NoteFieldNames.Body) or old_note.get(NoteFieldNames.Body).value
        self.tags = new_note.get(NoteFieldNames.Tags) or old_note.get(NoteFieldNames.Tags).value
        self.timestamp = old_note.get(NoteFieldNames.Time).value
    
    def realize(self) -> Note:
        self._tags_creator()
        self.note = Note(NoteId(self.id),Title(self.title),Body(self.body),Tags(self.tags),CreationTime(self.timestamp))
        return self.note
    
    def _tags_creator(self) -> None:
        if not isinstance(self.tags, list) and self.tags:
            self.tags = [tag.strip() for tag in self.tags.split(",")]
        elif not self.tags:
            self.tags = []
        

#MAIN CLASS ---------------------------------------       
class Notebook(UserList):
    def __init__(self,userlist: list[Note] = None):
        self.data = [] if not userlist else userlist
        
    def __repr__(self) -> str:
        return '\n'.join([str(note) for note in self.data])
    
    def add(self, title: str, body: str, tags:str = '') -> str:
        notecreator = NoteCreator(dict(title=title,body=body,tags=tags))
        note = notecreator.realize()
        self.data.append(note)
        return "Succesfuly added"
        
    def search(self, field: str, pattern: str) -> str:
        if field not in list(NoteFieldNames):
            return f'No field "{field}" in note'
        note_searcher = NoteSearcher(self.data)
        result = note_searcher.realize(field=field,pattern=pattern)
        if not result:
            return "No matches founded"
        return 'Here is what we found for your request:\n' + "\n".join([str(note) for note in result])
    
    def sort_notes(self, field: str, reverse: bool = False) -> str:
        if field not in list(NoteFieldNames):
            return f'No field "{field}" in note'
        
        note_sorter = NoteSorter(self.data)
        result = note_sorter.realize(field=field,reverse=reverse)
        return 'After sorting:\n' + "\n".join([str(note) for note in result])

    def delete(self, id: int) -> str:
        note = NoteSearcher(self.data).realize(NoteFieldNames.Id, id)
        if not note:
            return "No matches founded"
        self.data.remove(note[0])
        return "Succesfuly deleted"
    
    def delete_any(self, field: str, pattern:str) -> str:
        if field not in [NoteFieldNames.Title,NoteFieldNames.Body,NoteFieldNames.Tags]:
            return f"Can't use this function in field {field}"
        
        notes = NoteSearcher(self.data).realize(field, pattern=pattern)
        if not notes:
            return "No matches founded"
        
        for note in notes:
            self.data.remove(note)
        
        return "Succesfuly deleted"
            
    def delete_time_range(self, _from:datetime = None, _to: datetime = None) -> str:
        if not _from and not _to:
            return "Not correct range"
        
        range_founder = NoteInRangeFounder(self.data)
        notes_to_delete = range_founder.realize(_from,_to)
        if not notes_to_delete:
            return "Not correct range"
        
        for note in notes_to_delete:
            self.data.remove(note)
            
        return "Succesfuly deleted"

    def clear(self):
        self.data = []

    def edit(self, id: int, title: str = '', body: str = '', tags:str = '') -> str:
        
        searcher = NoteSearcher(self.data)
        old_note = searcher.realize(NoteFieldNames.Id, id)[0]     
        if not old_note:
            return f"No note with id: {id}" 
        
        note_editor = NoteEditor(old_note ,dict(title=title,body=body,tags=tags))
        new_note = note_editor.realize()
        self.data[self.data.index(old_note)] = new_note
        return f"Note with id: {id} succesfully changed"
    
    def change_start_id(self):
        max_id = max([note[NoteFieldNames.Id] for note in self.data])
        NoteCreator.note_id = max_id
    
    def to_list(self):
        return [note.to_dict() for note in self.data]

#FILE DOWNLOADER -----------------------------
class NotebookReader():
    def __init__(self, file: str):
        self.file = file
    
    def create(self) -> Notebook:
        try:
            with open(self.file,"r") as fl:
                notes_json = json.load(fl)
        except:
            return Notebook()
        
        notes = []
        for note_dict in notes_json:
            note = NoteCreator(note_dict).realize()
            notes.append(note)
        
        return Notebook(notes)
    
#FILE SAVER --------------------------------
class NotebookWriter():
    def __init__(self, file: str):
        self.file = file
    
    def write(self,notebook: Notebook):
        with open(self.file,"w") as fl:
            json.dump(notebook.to_list(),fl,indent=4,ensure_ascii=False)


def add_note(notebook: Notebook):
    title = input("Input title: ")
    body = input("Input body: ")
    tags = input('Input tags spliting by ",": ')
    print(notebook.add(title,body,tags))
    return notebook
    

if __name__ == "__main__":
    print("Create notebook")
    notebook = NotebookReader("/Users/macair/Desktop/GoIT - course/teem1__pr_1__/src/subordinate/Notes.json").create()
    notebook.change_start_id()
    notebook = add_note(notebook)
    notebook = add_note(notebook)
    notebook = add_note(notebook)
    
    print(notebook)
    print()
    print(notebook.delete(1))
    print()
    print(notebook)
    notebook = add_note(notebook)
    print(notebook.search("title","b"))
    # print(notebook.sort_notes("tags"))
    print(notebook.delete_any("body","yes"))
    # print(notebook.edit(2, "I","am","groot"))
    print(notebook)
    # notebook.clear()
    # print(notebook) 
    writer = NotebookWriter("/Users/macair/Desktop/GoIT - course/teem1__pr_1__/src/subordinate/Notes.json")
    writer.write(notebook)
