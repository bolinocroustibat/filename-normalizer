from pathlib import Path
from typing import TypeVar, Callable
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.console import Console
from .types import FileWithDate

T = TypeVar("T")


def scan_directory_with_parser(
    folder: Path,
    parser: Callable[[str], T | None],
    recursive: bool,
    console: Console,
) -> list[FileWithDate]:
    """
    Scan directory for files and apply a parser function to each filename.

    Args:
        folder: Directory to scan
        parser: Function that takes a filename and returns a result or None
        recursive: Whether to scan subdirectories
        console: Console object for progress display

    Returns:
        List of FileWithDate objects containing the file path and parsed date information
    """
    # Get all files in the directory
    if recursive:
        files: list[Path] = list(folder.rglob("*"))
    else:
        files: list[Path] = list(folder.glob("*"))

    # Filter only files (not directories)
    files = [f for f in files if f.is_file()]

    # Collect files with matching results
    matching_files: list[FileWithDate] = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning files...", total=len(files))
        for file_path in files:
            result: T | None = parser(file_path.name)
            if result is not None:
                # Unpack the tuple if result is a tuple
                if isinstance(result, tuple):
                    date, has_time = result
                    matching_files.append(FileWithDate(file_path, date, has_time))
                else:
                    # This case should not happen with parse_datetime_from_filename
                    # but kept for generic parser compatibility
                    matching_files.append(FileWithDate(file_path, result, False))
            progress.update(task, advance=1)

    return matching_files
