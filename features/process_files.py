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
from utils.types import File, FileType
from features.files_with_dates import (
    remove_date_patterns_from_filename,
)
from features.files_with_no_dates.find_date_in_pdf import find_date_in_pdf
from datetime import datetime
from pathlib import Path


def process_files(files: list[File], console: Console) -> tuple[int, int, int]:
    """Process files that need renaming and return counts of renamed, skipped, and already correct files.

    This function handles both files with dates in their names and PDF files without dates.
    For files with dates, it will clean the filename and rename it to YYYY-MM-DD format.
    For PDF files without dates, it will extract dates from their content using OpenAI.

    Args:
        files: List of files to process
        console: Console object for output

    Returns:
        tuple[int, int, int]: A tuple containing:
            - Number of files that were renamed
            - Number of files that were skipped (user declined or error)
            - Number of files that were already in the correct format
    """
    renamed_count = 0
    skipped_count = 0
    already_correct = 0

    # Create a single progress bar that will persist throughout the process
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Processing files...", total=len(files))
        
        for i, file in enumerate(files, 1):
            # Update progress before processing each file
            progress.update(task, completed=i-1)
            
            # Get the date either from filename or from PDF content
            if file.date is not None:
                # File already has a date from filename
                date = file.date
                has_time = file.has_time
                cleaned_filename = remove_date_patterns_from_filename(file.path.name)
                progress.console.print(
                    f"\nFound file with date: {file.path.absolute()}", style="bright_blue"
                )
            elif file.file_type == FileType.PDF:
                # Try to extract date from PDF content
                progress.console.print(
                    f"\nFound PDF without date: {file.path.absolute()}", style="bright_blue"
                )
                try:
                    date: datetime | None = find_date_in_pdf(file.path)
                    if date is None:
                        progress.console.print("No date found in PDF content", style="yellow")
                        skipped_count += 1
                        continue
                    has_time = False  # We don't extract time from PDF content
                    cleaned_filename = file.path.name  # Keep original filename
                    progress.console.print(
                        f"Found date in PDF: {date.strftime('%Y-%m-%d')}", style="green"
                    )
                except Exception as e:
                    progress.console.print(f"Error processing PDF: {str(e)}", style="red")
                    skipped_count += 1
                    continue
            else:
                # Skip files without dates that aren't PDFs
                continue

            # Rename files with found dates (either from filename or PDF)
            new_filename: str = generate_filename(cleaned_filename, date, has_time)
            new_path: Path = file.path.parent / new_filename

            # Skip if the new name is identical to the old name
            if new_filename == file.path.name:
                already_correct += 1
                continue

            # Temporarily hide the progress bar for the confirmation
            progress.stop()
            should_rename = typer.confirm(f"Rename '{file.path.name}' to '{new_filename}'?")
            progress.start()

            if should_rename:
                file.path.rename(new_path)
                progress.console.print(f"Renamed: {file.path.name} → {new_filename}", style="green")
                renamed_count += 1
            else:
                progress.console.print(f"Skipped: {file.path.name}", style="yellow")
                skipped_count += 1

    return renamed_count, skipped_count, already_correct
