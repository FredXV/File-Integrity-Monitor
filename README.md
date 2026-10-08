# File Integrity Monitor

A Python command-line security tool that detects unauthorised changes to files by comparing SHA-256 hashes against a saved baseline.

File integrity monitoring is a common security control: if a file's hash changes, its contents changed. This tool records a "known good" snapshot of a folder, then watches that folder and alerts you when files are modified, added or deleted.

## Features

- **Create Baseline**
  - Scans the `Monitored_files` folder (including subfolders)
  - Generates a SHA-256 hash for every file
  - Saves the hashes to `baseline.json`, so the baseline persists between runs
- **Run Integrity Check**
  - Re-scans the folder every 2 seconds and compares it to the baseline
  - Reports **modified** files, **new** files not in the baseline, and **deleted** files
  - Each change is reported once, so the output isn't flooded with repeat alerts
  - Press `Ctrl + C` to stop and return to the menu
- **View Baseline Data**
  - Prints the stored filename and hash for every monitored file
- **Exit**

### Error handling

- Unreadable files (e.g. permission errors) are skipped and listed as warnings instead of crashing the program
- A corrupted `baseline.json` is detected and handled with a clear message
- Files are hashed in 8 KB chunks, so large files don't need to fit in memory

## Project structure

```
File Integrity Monitor/
├── fim.py              # The file integrity monitor
├── Monitored_files/    # Folder that gets monitored
├── tests/
│   └── test_fim.py     # Pytest unit tests
└── baseline.json       # Created when you make a baseline (git-ignored)
```

## Getting started

**Requirements:** Python 3.8+ (standard library only, nothing to install for the tool itself)

```bash
git clone https://github.com/FredXV/File-Integrity-Monitor.git
cd File-Integrity-Monitor
```

Put the files you want to watch inside the `Monitored_files` folder, then run:

```bash
python fim.py
```

### Example workflow

1. Choose **1** to create a baseline of the current files
2. Choose **2** to start monitoring
3. Edit, add or delete a file in `Monitored_files` and watch the alert appear:

```
[WARNING] File has been modified: notes.txt
[ALERT] New file detected: report.docx
[ALERT] File deleted: old/config.ini
```

## Testing

The project has 11 unit tests in `tests/test_fim.py`, written with [pytest](https://pytest.org):

- **Hashing:** known SHA-256 values, empty files, identical and different content, and files larger than one chunk
- **Change detection:** unchanged, modified, added and deleted files, and an empty baseline
- **Folder scanning:** normal folders, subfolders and empty folders

Run them from the project folder:

```bash
pip install pytest
python -m pytest
```

## How it works

| Function | Purpose |
|---|---|
| `hash_file()` | Streams a file in chunks and returns its SHA-256 hex digest |
| `scan_folder()` | Walks a folder recursively and returns `{relative_path: hash}` plus any unreadable files |
| `compare()` | Compares baseline and current hashes and returns modified, added and deleted lists |
| `create_baseline()` / `load_baseline()` | Save and load the baseline as JSON |
| `check_integrity()` | Polling loop that reports changes |

## Limitations and future improvements

- Monitoring polls every 2 seconds rather than using real-time file system events (e.g. the `watchdog` library)
- `baseline.json` is stored unprotected, so someone with write access could alter it. Signing or protecting the baseline would improve security
- Only file contents are checked, not permissions or timestamps
- Possible additions: a configurable monitored folder, logging alerts to a file, and email notifications

## What I learned

- Structuring a program around a menu loop
- Generating SHA-256 hashes with `hashlib`
- Walking directories and handling file errors with `os`
- Persisting data between runs with `json`
- Variable scope and the `global` keyword
- Writing unit tests with `pytest` and `tmp_path` fixtures
- Debugging logic errors by tracing code step by step
- Using `.gitignore` to exclude generated files such as `baseline.json`
