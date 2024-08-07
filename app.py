import os
import shutil
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def delete_path(root_dir, relative_path):
    full_path = os.path.join(root_dir, relative_path)

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
    parser = argparse.ArgumentParser(description="Удаление файлов и папок из списка.")
    parser.add_argument("root_directory", type=str, help="Корневая папка для поиска.")
    parser.add_argument("list_file_path", type=str, help="Путь к файлу folders.txt.")
    parser.add_argument("--max_workers", type=int, default=10, help="Максимальное количество потоков.")

    args = parser.parse_args()

    delete_files_and_folders(args.root_directory, args.list_file_path, args.max_workers)