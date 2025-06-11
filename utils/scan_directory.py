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
from utils.types import File, FileType

T = TypeVar("T")


def scan_directory_with_parser(
    folder: Path,
    parser: Callable[[str], T | None],
    recursive: bool,
    console: Console,
) -> list[File]:
    """
    Scan directory for files and apply a parser function to each filename.

    Args:
        folder: Directory to scan
        parser: Function that takes a filename and returns a result or None
        recursive: Whether to scan subdirectories
        console: Console object for progress display

    Returns:
        List of File objects containing the file path and parsed information.
        Files with dates will have date and has_time set.
        PDF files without dates will have file_type set to PDF and date set to None.
    """
    # Get all files in the directory
    if recursive:
        files: list[Path] = list(folder.rglob("*"))
    else:
        files: list[Path] = list(folder.glob("*"))

    # Filter only files (not directories)
    files = [f for f in files if f.is_file()]

    # Collect files with matching results
    processed_files: list[File] = []

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
                    processed_files.append(
                        File(file_path, FileType.REGULAR, date, has_time)
                    )
                else:
                    # This case should not happen with parse_datetime_from_filename
                    # but kept for generic parser compatibility
                    processed_files.append(
                        File(file_path, FileType.REGULAR, result, False)
                    )
            elif file_path.suffix.lower() == ".pdf":
                # If no date found and it's a PDF, add it as a PDF file
                processed_files.append(File(file_path, FileType.PDF))
            progress.update(task, advance=1)

    return processed_files
