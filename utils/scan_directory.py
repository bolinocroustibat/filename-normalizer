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

T = TypeVar("T")

def scan_directory_with_parser(
    folder: Path,
    parser: Callable[[str], T | None],
    recursive: bool,
    console: Console,
) -> list[tuple[Path, T]]:
    """
    Scan directory for files and apply a parser function to each filename.
    
    Args:
        folder: Directory to scan
        parser: Function that takes a filename and returns a result or None
        recursive: Whether to scan subdirectories
        console: Console object for progress display
    
    Returns:
        List of tuples containing (file_path, parsing_result)
    """
    # Get all files in the directory
    if recursive:
        files: list[Path] = list(folder.rglob("*"))
    else:
        files: list[Path] = list(folder.glob("*"))

    # Filter only files (not directories)
    files = [f for f in files if f.is_file()]

    # Collect files with matching results
    matching_files: list[tuple[Path, T]] = []
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
                    matching_files.append((file_path, *result))
                else:
                    matching_files.append((file_path, result))
            progress.update(task, advance=1)

    return matching_files
