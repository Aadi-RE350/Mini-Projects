import json
from pathlib import Path
import shutil
import os


def load_log(log_file: Path) -> list:
    try:
        with log_file.open() as log:
            return json.load(log)

    except FileNotFoundError:
        raise ValueError(
            f"No previous changes found or '{log_file}' was moved."
        )

    except json.JSONDecodeError:
        raise ValueError(
            f"Error extracting JSON from '{log_file}'."
        )

def remove_empty_dir(dir_path: Path):
    try:
        dir_path.rmdir()
        print(f"Removed empty directory: {dir_path}")
    except OSError:
        pass

def restore_file(entry: dict):
    src = Path(entry["src"])
    des = Path(entry["des"])

    if des.exists():
        shutil.move(des, src)
        print(f"Restored: {des} -> {src}")

        remove_empty_dir(des.parent)
    else:
        print(f"Missing file: {des}")

def delete_log(log_file: Path):
    try:
        log_file.unlink()
        print(f"Deleted log file: {log_file}")
    except FileNotFoundError:
        pass

def undo(LOG_FILE):

    if not LOG_FILE:
        raise ValueError("Please add .env file and define LOG_FILE")

    log_path = Path(LOG_FILE)

    data = load_log(log_path)

    for entry in reversed(data):
        restore_file(entry)

    delete_log(log_path)

if __name__ == '__main__':
    undo('moves.json')