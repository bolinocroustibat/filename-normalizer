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
from utils.types import FileWithDate
from .remove_date_patterns import remove_date_patterns_from_filename


def process_matching_files(
    matching_files: list[FileWithDate], console: Console
) -> tuple[int, int, int]:
    """Process files that need renaming and return counts of renamed, skipped, and already correct files."""
    renamed_count = 0
    skipped_count = 0
    already_correct = 0

    for i, file_with_date in enumerate(matching_files, 1):
        # First clean the filename
        cleaned_filename = remove_date_patterns_from_filename(file_with_date.path.name)
        # Then generate the new filename
        new_filename = generate_filename(
            cleaned_filename, file_with_date.date, file_with_date.has_time
        )
        new_path = file_with_date.path.parent / new_filename

        # Skip if the new name is identical to the old name
        if new_filename == file_with_date.path.name:
            already_correct += 1
            continue

        # Display the full path in color
        console.print(
            f"\nFound file: {file_with_date.path.absolute()}", style="bright_blue"
        )

        if typer.confirm(f"Rename '{file_with_date.path.name}' to '{new_filename}'?"):
            file_with_date.path.rename(new_path)
            console.print(
                f"Renamed: {file_with_date.path.name} → {new_filename}", style="green"
            )
            renamed_count += 1
        else:
            console.print(f"Skipped: {file_with_date.path.name}", style="yellow")
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
            task = progress.add_task("Processing files...", total=len(matching_files))
            progress.update(task, completed=i)

    return renamed_count, skipped_count, already_correct
