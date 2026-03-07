import argparse
from pathlib import Path
import grp_ext

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


# group by extension
parser.add_argument('--group-by-ext', '--grp-by-ext', '--gbe',
                    action='store_true',
                    help='Group files by extension')


# --group-by-date
parser.add_argument('--group-by-date', '--grp-by-date', '--gbd',
                    action='store_true',
                    help='Group files by date')


# --dry-run
parser.add_argument('--dry-run',
                    action='store_true',
                    help='Only previews of the changes')

args = parser.parse_args()

if __name__ == '__main__':
    if not (args.group_by_ext or args.group_by_date):
        parser.error("Choose an operation: --group-by-ext or --group-by-date")

    if args.group_by_ext:
        grp_ext.by_ext(args.directory, args.dry_run)