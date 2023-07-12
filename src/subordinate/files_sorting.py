import os
import re
import shutil
from typing import List


def delete_empty_folders(dir_path: str, counter=0, hidd_except=True) -> int:
    """Recursively delete empty folders in such directory

    Args:
        dir_path (str): path to directory,
        counter (int, optional): start calculation number of deleted folders. Defaults to 0.,
        hidd_except (bool, optional): If True fuction ignores all hidden folders, if False - delete them too. Defaults to True.

    Returns:
        int: number of deleted folders
    """

    for element in os.scandir(dir_path):
        if hidd_except and element.name.startswith("."):
            continue
        if element.is_dir():
            try:
                os.rmdir(element.path)
            except OSError:
                counter += delete_empty_folders(element.path, counter)
            else:
                counter += 1
    return counter


def normalize(name: str) -> str:
    # Транслит
    trans = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "y",
        "ф": "f",
        "х": "x",
        "ц": "c",
        "ч": "ch",
        "э": "a",
        "ю": "u",
        "я": "ya",
    }
    # латиница
    name = name.translate(trans)
    # все символы кроме латинских букв и цифр на пробел
    name = re.sub(r"[^\w]", "_", name)
    return name


def sort_files(path: str):
    # Список расширений файлов по категориям
    images = ["JPEG", "PNG", "JPG", "SVG"]
    videos = ["AVI", "MP4", "MOV", "MKV"]
    documents = ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"]
    music = ["MP3", "OGG", "WAV", "AMR"]
    archives = ["ZIP", "GZ", "TAR"]

    # Словарь для хранения файлов по категориям
    files_by_category = {
        "images": [],
        "videos": [],
        "documents": [],
        "music": [],
        "archives": [],
        "unknown": [],
    }

    # Словарь разрешений:
    extensions = {"known": set(), "unknown": set()}

    # папки для каждой категории файлов
    for category in files_by_category.keys():
        if not os.path.exists(os.path.join(path, category)):
            os.mkdir(os.path.join(path, category))

    # Обходим все файлы и папки в указанной директории
    for dirpath, dirnames, filenames in os.walk(path):
        # Игнор папок : archives, video, audio, documents, images!
        if os.path.basename(dirpath) in files_by_category.keys():
            continue

        for filename in filenames:
            # расширение файла
            extension = filename.split(".")[-1].upper()

            # категория файла по расширению
            if extension in images:
                category = "images"
                extensions["known"].add(extension)
            elif extension in videos:
                category = "videos"
                extensions["known"].add(extension)
            elif extension in documents:
                category = "documents"
                extensions["known"].add(extension)
            elif extension in music:
                category = "music"
                extensions["known"].add(extension)
            elif extension in archives:
                category = "archives"
                extensions["known"].add(extension)

                # Распаковка архивов
                folder_name = os.path.join(path, category, filename.split(".")[0])
                shutil.unpack_archive(os.path.join(dirpath, filename), folder_name)
            else:
                category = "unknown"
                extensions["unknown"].add(extension)

            # Добавляем файл в соответствующую категорию
            files_by_category[category].append(filename)

            # Нормализуем имя файла и переименовываем его
            new_filename = normalize(filename.split(".")[0]) + "." + filename.split(".")[-1]
            os.rename(
                os.path.join(dirpath, filename), os.path.join(dirpath, new_filename)
            )

            # не сортированные
            if category != "unknown":
                nw_folder_path = os.path.join(path, category)
                if os.path.exists(os.path.join(nw_folder_path, new_filename)):
                    continue
                shutil.move(
                    os.path.join(dirpath, new_filename), os.path.join(path, category)
                )

        # пустые папки del
        if not os.listdir(dirpath):
            os.rmdir(dirpath)

    # итог:
    print("Files by category:")
    for category, files in files_by_category.items():
        print(f"{category.capitalize()}:")
        for file in files:
            print(f"  {file}")

    print("\nKnown extensions:")
    for ext in sorted(extensions["known"]):
        print(f"  {ext}")

    print("\nUnknown extensions:")
    for ext in sorted(extensions["unknown"]):
        print(f"  {ext}")


def main_sorting():
    
    dir_path = input("Enter the folder path: ")
    if not os.path.isdir(dir_path):
        print("Invalid path entered")
    
    sort_files(dir_path)
    delete_empty_folders(dir_path)