from pathlib import Path
from datetime import datetime
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.console import Console
from .parse import parse_datetime_from_filename


def scan_directory_for_date_patterns(
    folder: Path, recursive: bool, console: Console
) -> list[tuple[Path, datetime, bool]]:
    """Scan directory for files with date patterns and return matching files."""
    # Get all files in the directory
    if recursive:
        files = list(folder.rglob("*"))
    else:
        files = list(folder.glob("*"))

    # Filter only files (not directories)
    files = [f for f in files if f.is_file()]

    # Collect files with date patterns
    matching_files = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning files...", total=len(files))
        for file_path in files:
            result = parse_datetime_from_filename(file_path.name)
            if result:
                matching_files.append((file_path, *result))
            progress.update(task, advance=1)

    return matching_files
