import typer
from pathlib import Path
from rich.console import Console
from dotenv import load_dotenv
from utils import scan_directory_with_parser
from utils.types import File
from utils.summary import print_summary
from features.files_with_dates import parse_datetime_from_filename
from features.process_files import process_files
from utils.logger import FileLogger

# Load environment variables at startup
load_dotenv()

app = typer.Typer()
console = Console()
logger = FileLogger("main")


@app.command()
def main(
    folder: Path = typer.Argument(
        ..., help="Folder to search for files with date patterns"
    ),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Search recursively in subfolders"
    ),
):
    """
    Search for files with date patterns in their names and offer to rename them to YYYY-MM-DD format.
    """
    if not folder.exists():
        logger.error(f"Folder '{folder}' does not exist")
        raise typer.Exit(1)

    if not folder.is_dir():
        logger.error(f"'{folder}' is not a directory")
        raise typer.Exit(1)

    # Scan for files
    files: list[File] = scan_directory_with_parser(
        folder, parse_datetime_from_filename, recursive, console
    )

    if not files:
        logger.info("No files found.")
        return

    # Process all files
    renamed_count: int
    skipped_count: int
    already_correct: int
    renamed_count, skipped_count, already_correct = process_files(files, console)

    # Print summary
    print_summary(renamed_count, skipped_count, already_correct, len(files))


if __name__ == "__main__":
    app()
