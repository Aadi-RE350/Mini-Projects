import shutil
from pathlib import Path
import json
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

IGNORE_FILES = {f.strip() for f in os.getenv("IGNORE_FILES","").split(",") if f}

def load_moves(logfile:Path)->list:
    if logfile.exists():
        try:
            with open(logfile) as log:
                return json.load(log)
        except json.JSONDecodeError:
            return []
    return []


def get_date(file: Path) -> tuple[str, str]: #year,month
    stat = file.stat()
    try:
        birth_sec = stat.st_birthtime
    except AttributeError:
        birth_sec = stat.st_mtime  # fallback

    dt_object = datetime.fromtimestamp(birth_sec)
    return str(dt_object.year),dt_object.strftime('%b')


def process_file(file:Path,dirpath:Path,moves:list,is_dry:bool)->tuple[int,int]:
    year,month = get_date(file)

    des_dir = dirpath / year / month
    des_path = des_dir / file.name

    if des_path.exists():
        print(f"Skipping existing file: {des_path}")
        return 0,1
    
    if not is_dry:
        moves.append({
            "src": str(file),
            "des": str(des_path)
        })
        des_dir.mkdir(parents=True,exist_ok=True)
        shutil.copy2(file,des_path) #only for testing
    else:
        print(f"[DRY RUN] {file} -> {des_path}")
    return 1,0


def save_moves(logfile:Path,moves:list):
    with open(logfile,'w') as f:
        json.dump(moves,f,indent=4)

def by_date(dirpath:Path,is_dry:bool):
    if not dirpath.is_dir():
        raise ValueError('Argument provided must be a directory')
    
    # load moves
    logfile = dirpath / 'moves.json'
    moves = load_moves(logfile)

    skipped = 0
    moved = 0

    # process 
    for file in dirpath.iterdir():
        if not file.is_file() or file.name in IGNORE_FILES or file.is_symlink():
            continue

        m,s = process_file(file,dirpath,moves,is_dry)
        moved += m
        skipped += s
    
    if not is_dry:
        save_moves(logfile,moves)
    
    print(f'\nSummary : {moved} files moved, {skipped} files skipped\n')



if __name__ == "__main__":
    by_date(Path('.'),False)

