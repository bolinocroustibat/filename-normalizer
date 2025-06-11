import typer
from pathlib import Path
from rich.console import Console
from features.files_with_dates import (
    scan_directory_for_date_patterns,
    process_matching_files,
    print_summary,
)

app = typer.Typer()
console = Console()


@app.command()
def main(
    folder: Path = typer.Argument(
        ..., help="Folder to search for files with date patterns"
    ),
    recursive: bool = typer.Option(
        True, "--recursive", "-r", help="Search recursively in subfolders"
    ),
):
    """
    Search for files with date patterns in their names and offer to rename them to YYYY-MM-DD format.
    """
    if not folder.exists():
        console.print(f"Error: Folder '{folder}' does not exist", style="red")
        raise typer.Exit(1)

    if not folder.is_dir():
        console.print(f"Error: '{folder}' is not a directory", style="red")
        raise typer.Exit(1)

    # Scan for files with date patterns
    matching_files = scan_directory_for_date_patterns(folder, recursive, console)

    if not matching_files:
        console.print("No files with date patterns found.")
        return

    # Process matching files
    renamed_count, skipped_count, already_correct = process_matching_files(
        matching_files, console
    )

    # Print summary
    print_summary(
        renamed_count, skipped_count, already_correct, len(matching_files), console
    )


if __name__ == "__main__":
    app()
