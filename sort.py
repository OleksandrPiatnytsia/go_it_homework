from pathlib import Path


def delete_empty_folders(path):
    root_folder = Path(path)

    if not root_folder.exists():
        # print(f"Пропускаємо не існує:{root_folder}")
        return None

    if root_folder.is_dir() and root_folder.name not in get_format_dict():

        if not any(root_folder.iterdir()):

            print(f"Deleting empty folder: {root_folder}")

            parent_folder_name = root_folder.parent

            root_folder.rmdir()

            delete_empty_folders(parent_folder_name)
        else:
            for include_file in root_folder.iterdir():
                delete_empty_folders(include_file)


def attach_path(path, folder):
    if path.endswith("\\"):
        return path + folder
    else:
        return path + "\\" + folder


def get_format_dict():
    return {"images": ['.JPEG', '.PNG', '.JPG', '.SVG'],
            "documents": ['.TXT', '.DOC', '.XLS', '.XLSX'],
            "python": ['.PY'],
            "audio": ['.MP3', '.OGG', '.WAV', '.AMR'],
            "video": ['.AVI', '.MP4', '.MOV', '.MKV'],
            "archives": ['.ZIP', '.GZ', '.TAR'],
            "oather": []
            }


def normalize_dir(path):
    path_list = path.strip("\\").split("\\")
    last_dir = translate(path_list[-1])
    path_list.pop()
    path_list.append(last_dir)
    for tmp_dir in path_list[1:]:
        normalize(tmp_dir)

    return "\\".join(path_list)


def sort_folders(main_path: str, path: str):
    root_folder = Path(path)

    if not root_folder.exists():
        # print(f"Folder {path} was empty and was deleted!")
        return None

    if not root_folder.exists():
        # print(f"Пропускаємо не існує:{root_folder}")
        return None

    if main_path == path:

        # створюємо папки
        formats_dict = get_format_dict()

        for groupe_format in formats_dict:
            new_folder = Path(attach_path(main_path, groupe_format))
            new_folder.mkdir(exist_ok=True)

    for include_file in root_folder.iterdir():

        if include_file.is_dir():
            if include_file.name not in get_format_dict():
                sort_folders(main_path, include_file)

        else:

            if include_file.exists():
                formats_dict = get_format_dict()

                folder_name_taken = ""
                for folder_name, format_list in formats_dict.items():

                    if include_file.suffix.upper() in format_list:
                        folder_name_taken = folder_name
                        break

                if not folder_name_taken:
                    folder_name = "oather"

                count = 0
                while True:

                    if not count:
                        new_file_name = include_file.name.replace(include_file.suffix, "")
                    else:
                        new_file_name = include_file.name.replace(include_file.suffix, "") + "_" + str(
                            count)

                    if folder_name == "archives":
                        new_file_name = normalize(translate(new_file_name))
                    else:
                        new_file_name = normalize(translate(new_file_name)) + include_file.suffix

                    replaced_file = Path(attach_path(main_path, folder_name) + "\\" + new_file_name)

                    if replaced_file.exists():
                        count += 1
                    else:
                        break

                if folder_name == "archives":

                    # У випадку архіва, розпаковуємо unpack_archive() його в одноіменну папку та виділяємо архів через unlink()
                    import shutil

                    replaced_file.mkdir()

                    shutil.unpack_archive(include_file, replaced_file)
                    include_file.unlink()

                else:
                    include_file.rename(replaced_file)

    delete_empty_folders(path)

def get_translate_dict():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "y", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    return TRANS


def translate(text: str):
    TRANS = get_translate_dict()
    result = ""

    for char_ in text:

        if ord(char_) in TRANS:
            result += TRANS.get(ord(char_))
        else:
            result += char_

    return result


def main():

    import sys
    path = sys.argv[1:2]
    path = path[0]

    # path = r"C:\Temp\test"

    if not path:
        print(f"Path for sorting is empty!")
        return None

    print(f'Sorting folder: "{path}" is started')

    # Номалізуємо каталоги

    root_folder = Path(path)
    if root_folder.exists():
        path = normalize_dir(path)
        root_folder.rename(path)

        for parent in root_folder.parents:
            if not parent == parent.parent:

                new_dir_path = normalize_dir(str(parent))
                if new_dir_path != str(parent):
                    parent_folder = Path(str(parent))
                    parent_folder.rename(new_dir_path)

        sort_folders(path, path)

    print(f'Sorting folder: "{path}" is complete')

    total_files = 0

    formats_dict = get_format_dict()

    for groupe_format in formats_dict:
        folder = Path(attach_path(path, groupe_format))
        # print(f'Files category "{folder.name}" : {len(include_folder.glob("*"))}')
        files_count = 0
        for _ in folder.iterdir():
            files_count += 1

        total_files += files_count

        print(f'Files category "{folder.name}": {files_count}')

    print(f'Total count of sorted files: {total_files}')

def normalize(text: str):
    import re
    text = translate(text)

    text = re.sub(r"[^a-zA-Z0-9]+", "_", text)

    return text


if __name__ == "__main__":
    main()
