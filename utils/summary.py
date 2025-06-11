from rich.console import Console


def print_summary(
    renamed_count: int,
    skipped_count: int,
    already_correct: int,
    total_files: int,
    console: Console,
) -> None:
    """Print a summary of the renaming operations."""
    console.print("\nSummary:", style="bold")
    console.print(f"Files already in correct format: {already_correct}", style="blue")
    console.print(f"Files renamed: {renamed_count}", style="green")
    console.print(f"Files skipped: {skipped_count}", style="yellow")
    console.print(f"Total files processed: {total_files}", style="bold")
