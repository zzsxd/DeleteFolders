import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed


def delete_path(root_dir, relative_path):
    full_path = os.path.join(root_dir, relative_path).replace("\\", "/")

    if os.path.exists(full_path):
        try:
            if os.path.isfile(full_path):
                os.remove(full_path)
                return f"Файл удален: {full_path}"
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
                return f"Папка удалена: {full_path}"
        except Exception as e:
            return f"Ошибка при удалении {full_path}: {e}"
    else:
        return f"Путь не существует: {full_path}"


def delete_files_and_folders(root_dir, list_file, max_workers=10):
    try:
        with open(list_file, 'r') as f:
            paths = f.read().splitlines()
    except Exception as e:
        print(f"Ошибка при чтении файла {list_file}: {e}")
        return

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(delete_path, root_dir, path): path for path in paths}

        for future in as_completed(future_to_path):
            result = future.result()
            print(result)


if __name__ == "__main__":
    root_directory = input("Корневая папка для поиска: ")
    list_file_path = input("Путь к файлу с папками и файлами для удаления: ")
    max_threads = int(input("Количество потоков: "))

    delete_files_and_folders(root_directory, list_file_path, max_threads)