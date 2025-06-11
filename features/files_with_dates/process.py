from pathlib import Path
from datetime import datetime
import typer
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.console import Console
from utils import generate_filename
from .remove_date_patterns import remove_date_patterns_from_filename


def process_matching_files(
    matching_files: list[tuple[Path, datetime, bool]], console: Console
) -> tuple[int, int, int]:
    """Process files that need renaming and return counts of renamed, skipped, and already correct files."""
    renamed_count = 0
    skipped_count = 0
    already_correct = 0

    for i, (file_path, new_datetime, has_time) in enumerate(matching_files, 1):
        # First clean the filename
        cleaned_filename = remove_date_patterns_from_filename(file_path.name)
        # Then generate the new filename
        new_filename = generate_filename(cleaned_filename, new_datetime, has_time)
        new_path = file_path.parent / new_filename

        # Skip if the new name is identical to the old name
        if new_filename == file_path.name:
            already_correct += 1
            continue

        # Display the full path in color
        console.print(f"\nFound file: {file_path.absolute()}", style="bright_blue")

        if typer.confirm(f"Rename '{file_path.name}' to '{new_filename}'?"):
            file_path.rename(new_path)
            console.print(f"Renamed: {file_path.name} → {new_filename}", style="green")
            renamed_count += 1
        else:
            console.print(f"Skipped: {file_path.name}", style="yellow")
            skipped_count += 1

        # Show progress after each file
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Processing files...", total=len(matching_files))
            progress.update(task, completed=i)

    return renamed_count, skipped_count, already_correct
