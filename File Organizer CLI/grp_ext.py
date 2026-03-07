from pathlib import Path
import shutil
import mimetypes
import json
from dotenv import load_dotenv
import os

load_dotenv()

IGNORE_FILES = {f.strip() for f in os.getenv("IGNORE_FILES","").split(",") if f}

def load_moves(log_file:Path)->list:
    if log_file.exists():
        try:
            with open(log_file) as log:
                return json.load(log)
        except json.JSONDecodeError:
            return []
    return []


def get_category(file:Path)->str:
    mimetype = mimetypes.guess_type(str(file))[0]
    if mimetype:
        category = mimetype.split('/')[0]
    else:
        category = 'Unknown'
    return category

def process_file(file:Path,dirpath:Path,is_dry:bool,moves:list):
    category = get_category(file)
    des_dir = dirpath / category
    des_path = des_dir / file.name
    if des_path.exists():
        print(f"Skipping existing file: {des_path}")
        return

    if not is_dry:
        moves.append({
            "src": str(file),
            "des": str(des_path)
        })
        des_dir.mkdir(exist_ok=True)
        shutil.copy2(file,des_path)
    else:
        print(f"[DRY RUN] {file} -> {des_path}")

def save_moves(log_file:Path,moves:list):
    with open(log_file,'w') as f:
        json.dump(moves,f,indent=4)

def by_ext(dirpath:Path,is_dry:bool):
    if not dirpath.is_dir():
        raise ValueError('Argument provided is not a directory')

    log_file = dirpath / 'moves.json'
    moves = load_moves(log_file)

    for file in dirpath.iterdir():
        if not file.is_file():
            continue

        if file.name in IGNORE_FILES:
            continue

        if file.parent != dirpath:
            continue

        process_file(file,dirpath,is_dry,moves)
    
    if not is_dry:
        save_moves(log_file,moves)


if __name__ == "__main__":
    dirpath = Path('./')
    by_ext(dirpath,True)