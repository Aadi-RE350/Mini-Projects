import argparse
from pathlib import Path
import grp_ext
import grp_date
from undo import undo
from dotenv import load_dotenv
import os

load_dotenv()

IGNORE_FILES = {f.strip() for f in os.getenv("IGNORE_FILES","").split(",") if f}
LOGFILE = (os.getenv('LOG_FILE') or 'moves.json').strip()
IGNORE_FILES.add(LOGFILE)

parser = argparse.ArgumentParser(
    prog='File Organizer CLI',
    description='Build a command-line tool that scans a given directory and moves files into organized subdirectories.'
)

# Directory path
parser.add_argument(
    'directory',
    nargs='?',
    default=Path.cwd(),
    type=Path,
    help='Directory path (default: current directory)'
)

# dry run
parser.add_argument(
    '--dry-run',
    action='store_true',
    help='Preview changes without moving files'
)

# operations
operations = parser.add_mutually_exclusive_group(required=True)

operations.add_argument(
    '--group-by-ext', '--grp-by-ext', '--gbe',
    action='store_true',
    help='Group files by extension'
)

operations.add_argument(
    '--group-by-date', '--grp-by-date', '--gbd',
    action='store_true',
    help='Group files by date'
)

operations.add_argument(
    '--undo',
    action='store_true',
    help='Undo the last file organization using the log file'
)

args = parser.parse_args()

if __name__ == '__main__':

    if args.group_by_ext:
        grp_ext.by_ext(args.directory, args.dry_run, LOGFILE, IGNORE_FILES)

    elif args.group_by_date:
        grp_date.by_date(args.directory, args.dry_run, LOGFILE, IGNORE_FILES)

    elif args.undo:
        undo(LOGFILE)