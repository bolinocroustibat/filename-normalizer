# Filename Normalizer

A command-line tool to automatically detect and standardize date and time patterns in filenames. This tool helps organize your files by converting various formats into a consistent YYYY-MM-DD or YYYY-MM-DD_HH-MM-SS format.

## Features

- Detects and standardizes multiple date formats in filenames:
  - YYYY-MM-DD or YYYY_MM_DD
  - DD-MM-YYYY or DD_MM_YYYY
  - DD-MM-YY or DD_MM_YY
  - M-D-YYYY or M_D_YYYY
  - M-D-YY or M_D_YY
- Detects and standardizes time formats:
  - HH:MM:SS or HH.MM.SS
  - HH:MM or HH.MM
- Interactive renaming with confirmation prompts
- Recursive directory search
- Preserves original filename while standardizing the date format
- Color-coded output for better visibility

## Installation

```bash
# Install dependencies
uv sync
```

## Usage

Basic usage:
```bash
uv run main.py /path/to/your/folder
```

Search in current directory only (non-recursive):
```bash
uv run main.py /path/to/your/folder --no-recursive
```

### Example

If you have files like:
```
vacation_2023-12-25.jpg
IMG_25-12-2023_15-30-00.jpg
photo_12-25-23.jpg
meeting_2024-01-15_14-30.jpg
```

The tool will offer to rename them to:
```
2023-12-25_vacation.jpg
2023-12-25_15-30-00_IMG.jpg
2023-12-25_photo.jpg
2024-01-15_14-30_meeting.jpg
```

## Requirements

- Python 3.10 or higher
- typer
- ruff (for development)

## License

MIT License
