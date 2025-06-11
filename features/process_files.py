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


def process_files(files: list[File], console: Console) -> tuple[int, int, int]:
    """Process files that need renaming and return counts of renamed, skipped, and already correct files.

    This function handles both files with dates in their names and PDF files without dates.
    For files with dates, it will clean the filename and rename it to YYYY-MM-DD format.
    For PDF files without dates, it will prepare for future date extraction from content.
    """
    renamed_count = 0
    skipped_count = 0
    already_correct = 0

    for i, file in enumerate(files, 1):
        if file.date is not None:
            # Process files with dates
            cleaned_filename = remove_date_patterns_from_filename(file.path.name)
            new_filename = generate_filename(cleaned_filename, file.date, file.has_time)
            new_path = file.path.parent / new_filename

            # Skip if the new name is identical to the old name
            if new_filename == file.path.name:
                already_correct += 1
                continue

            # Display the full path in color
            console.print(
                f"\nFound file with date: {file.path.absolute()}", style="bright_blue"
            )

            if typer.confirm(f"Rename '{file.path.name}' to '{new_filename}'?"):
                file.path.rename(new_path)
                console.print(
                    f"Renamed: {file.path.name} → {new_filename}", style="green"
                )
                renamed_count += 1
            else:
                console.print(f"Skipped: {file.path.name}", style="yellow")
                skipped_count += 1

        elif file.file_type == FileType.PDF:
            # TODO: Process PDF files without dates
            # This will be implemented when we add PDF date extraction
            console.print(
                f"\nFound PDF without date: {file.path.absolute()}", style="bright_blue"
            )
            console.print("PDF date extraction not yet implemented", style="yellow")
            skipped_count += 1

        # Show progress after each file
        console.print()  # Add a line break before the progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Processing files...", total=len(files))
            progress.update(task, completed=i)

    return renamed_count, skipped_count, already_correct
