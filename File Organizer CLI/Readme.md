## Description
Build a command-line tool that scans a given directory and moves files into organized subdirectories. The user should be able to choose the grouping strategy — by file extension (.jpg, .pdf…), by creation month, or by detected MIME type. This is your first real Python project with a proper CLI interface and file system operations.
## Minimum Requirements
1. Accept a target directory path as a CLI argument
2. Group files by extension into subdirectories (e.g. images/docs/)
3. Implement a --dry-run flag that previews moves without executing them
4. Print a summary: N files moved, N skipped, N errors
5. Handle edge cases: symlinks, empty files, permission errors
## Bonus Challenges
- Add --group-by-date to sort by year/month
- Use python-magic for MIME-based grouping instead of extension
- Write a config file (organizer.toml) for custom rules
- Add undo functionality by logging moves to a JSON file
## Execution example
A pip-installable CLI: `organize ~/Downloads --group-by-ext --dry-run `