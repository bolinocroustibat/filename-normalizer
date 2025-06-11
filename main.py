import typer
from pathlib import Path
from rich.console import Console
from utils import scan_directory_with_parser
from utils.types import File
from utils.summary import print_summary
from features.files_with_dates import parse_datetime_from_filename
from features.process_files import process_files

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

    # Scan for files
    files: list[File] = scan_directory_with_parser(
        folder, parse_datetime_from_filename, recursive, console
    )

    if not files:
        console.print("No files found.")
        return

    # Process all files
    renamed_count: int
    skipped_count: int
    already_correct: int
    renamed_count, skipped_count, already_correct = process_files(files, console)

    # Print summary
    print_summary(renamed_count, skipped_count, already_correct, len(files), console)


if __name__ == "__main__":
    app()
