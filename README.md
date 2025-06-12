# Filename Normalizer

A tool to normalize filenames by extracting dates from filenames or PDF content and renaming them to a consistent format.

## Features

- Extract dates from filenames using various date patterns
- Extract dates from PDF content using OpenAI's GPT-4
- Rename files to a consistent YYYY-MM-DD format
- Handle both files with dates in names and PDFs without dates
- Colored logging output with configurable log levels

## Installation

1. Clone the repository
2. Install dependencies:
```bash
uv sync
```

## Environment Setup

Create a `.env` file in the project root with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_API_MODEL=gpt-4-turbo-preview  # Optional, defaults to gpt-4-turbo-preview

# Logging Configuration
LOG_LEVEL=INFO  # Optional, defaults to INFO. Can be DEBUG, INFO, WARNING, ERROR
```

You can get an API key from [OpenAI's platform](https://platform.openai.com/api-keys).

## Usage

```bash
uv run main.py /path/to/your/folder [--recursive]
```

Options:
- `--recursive`, `-r`: Search recursively in subfolders (default: False)

## How it works

1. The tool scans the specified directory for files
2. For each file:
   - If it has a date in its name, it will be renamed to YYYY-MM-DD format
   - If it's a PDF without a date in its name, it will try to extract a date from its content using OpenAI
3. You'll be prompted to confirm each rename operation
4. A summary of processed files will be displayed at the end

## Logging

The tool provides detailed logging with colored output:
- Logs are saved in the `logs` directory
- Log level can be configured via `LOG_LEVEL` environment variable
- Available log levels: DEBUG, INFO, WARNING, ERROR
- Each component has its own log file:
  - `pdf_analyzer.log`: OpenAI API interactions
  - `pdf_finder.log`: PDF processing coordination
  - `pdf_extractor.log`: PDF text extraction

## Requirements

- Python 3.10 or higher
- typer
- ruff (for development)

## License

MIT License
