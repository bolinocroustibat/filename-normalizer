import typer
from pathlib import Path
import re
from datetime import datetime
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.console import Console

app = typer.Typer()
console = Console()

def parse_datetime_from_filename(filename: str) -> tuple[datetime, bool] | None:
    # Common date patterns in filenames
    date_patterns = [
        r'(\d{4})[-_](\d{2})[-_](\d{2})',  # YYYY-MM-DD or YYYY_MM_DD
        r'(\d{2})[-_](\d{2})[-_](\d{4})',  # DD-MM-YYYY or DD_MM_YYYY
        r'(\d{2})[-_](\d{2})[-_](\d{2})',   # DD-MM-YY or DD_MM_YY
        r'(\d{1,2})[-_](\d{1,2})[-_](\d{4})',  # M-D-YYYY or M_D_YYYY
        r'(\d{1,2})[-_](\d{1,2})[-_](\d{2})',  # M-D-YY or M_D_YY
    ]
    
    # Common time patterns in filenames
    time_patterns = [
        r'(\d{1,2})[.:](\d{2})[.:](\d{2})',  # HH:MM:SS or HH.MM.SS
        r'(\d{1,2})[.:](\d{2})',  # HH:MM or HH.MM
    ]
    
    # Try date patterns first
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            try:
                # Handle YYYY-MM-DD format
                if len(match.group(1)) == 4:
                    year = int(match.group(1))
                    month = int(match.group(2))
                    day = int(match.group(3))
                else:
                    # Handle other formats
                    if len(match.group(3)) == 2:  # If year is 2 digits
                        year = int(match.group(3))
                        if year < 50:  # Assuming years 00-49 are 2000-2049
                            year += 2000
                        else:  # Assuming years 50-99 are 1950-1999
                            year += 1900
                    else:
                        year = int(match.group(3))
                    
                    month = int(match.group(2))
                    day = int(match.group(1))
                
                # Check if there's a time pattern after the date
                time_match = None
                for time_pattern in time_patterns:
                    time_match = re.search(time_pattern, filename[match.end():])
                    if time_match:
                        break
                
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2))
                    second = int(time_match.group(3)) if len(time_match.groups()) > 2 else 0
                    return datetime(year, month, day, hour, minute, second), True
                else:
                    return datetime(year, month, day), False
            except ValueError:
                continue
    return None

def rename_file(file_path: Path, new_datetime: datetime, has_time: bool) -> bool:
    # Get the original filename without the date
    filename = file_path.name
    
    # Remove the date pattern from the filename
    date_patterns = [
        r'\d{4}[-_]\d{2}[-_]\d{2}',  # YYYY-MM-DD or YYYY_MM_DD
        r'\d{2}[-_]\d{2}[-_]\d{4}',  # DD-MM-YYYY or DD_MM_YYYY
        r'\d{2}[-_]\d{2}[-_]\d{2}',   # DD-MM-YY or DD_MM_YY
        r'\d{1,2}[-_]\d{1,2}[-_]\d{4}',  # M-D-YYYY or M_D_YYYY
        r'\d{1,2}[-_]\d{1,2}[-_]\d{2}',  # M-D-YY or M_D_YY
    ]
    
    # Remove time patterns
    time_patterns = [
        r'\d{1,2}[.:]\d{2}[.:]\d{2}',  # HH:MM:SS or HH.MM.SS
        r'\d{1,2}[.:]\d{2}',  # HH:MM or HH.MM
    ]
    
    for pattern in date_patterns:
        # Remove the date pattern and any surrounding spaces or underscores
        filename = re.sub(r'[\s_]*' + pattern + r'[\s_]*', '', filename)
    
    for pattern in time_patterns:
        # Remove the time pattern and any surrounding spaces or underscores
        filename = re.sub(r'[\s_]*' + pattern + r'[\s_]*', '', filename)
    
    # Clean up any double spaces that might have been left
    filename = re.sub(r'\s+', ' ', filename)  # Replace multiple spaces with single space
    filename = filename.strip(' ')  # Remove leading/trailing spaces
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove leading underscore if present
    filename = filename.lstrip('_')
    
    # Create new filename with standardized date format
    if has_time:
        new_filename = f"{new_datetime.strftime('%Y-%m-%d_%H-%M-%S')}_{filename}"
    else:
        new_filename = f"{new_datetime.strftime('%Y-%m-%d')}_{filename}"
    
    new_path = file_path.parent / new_filename
    
    # Skip if the new name is identical to the old name
    if new_filename == file_path.name:
        return False
    
    # Display the full path in color
    console.print(f"Found file: {file_path.absolute()}", style="bright_blue")
    
    # Debug print before confirmation
    console.print("DEBUG: About to ask for confirmation", style="yellow")
    
    if typer.confirm(f"Rename '{file_path.name}' to '{new_filename}'?"):
        # Debug print after confirmation
        console.print("DEBUG: User confirmed", style="green")
        file_path.rename(new_path)
        console.print(f"Renamed: {file_path.name} → {new_filename}", style="green")
        return True
    else:
        # Debug print after skipping
        console.print("DEBUG: User skipped", style="yellow")
        console.print(f"Skipped: {file_path.name}", style="yellow")
        return False

@app.command()
def main(
    folder: Path = typer.Argument(..., help="Folder to search for files with date patterns"),
    recursive: bool = typer.Option(True, "--recursive", "-r", help="Search recursively in subfolders")
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
    
    # Get all files in the directory
    if recursive:
        files = list(folder.rglob("*"))
    else:
        files = list(folder.glob("*"))
    
    # Filter only files (not directories)
    files = [f for f in files if f.is_file()]
    
    # First pass: collect files with date patterns
    matching_files = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning files...", total=len(files))
        for file_path in files:
            result = parse_datetime_from_filename(file_path.name)
            if result:
                matching_files.append((file_path, *result))
            progress.update(task, advance=1)
    
    if not matching_files:
        console.print("No files with date patterns found.")
        return
    
    # Process matching files
    renamed_count = 0
    skipped_count = 0
    already_correct = 0
    
    for file_path, new_datetime, has_time in matching_files:
        # Get the original filename without the date
        filename = file_path.name
        
        # Remove the date pattern from the filename
        date_patterns = [
            r'\d{4}[-_]\d{2}[-_]\d{2}',  # YYYY-MM-DD or YYYY_MM_DD
            r'\d{2}[-_]\d{2}[-_]\d{4}',  # DD-MM-YYYY or DD_MM_YYYY
            r'\d{2}[-_]\d{2}[-_]\d{2}',   # DD-MM-YY or DD_MM_YY
            r'\d{1,2}[-_]\d{1,2}[-_]\d{4}',  # M-D-YYYY or M_D_YYYY
            r'\d{1,2}[-_]\d{1,2}[-_]\d{2}',  # M-D-YY or M_D_YY
        ]
        
        # Remove time patterns
        time_patterns = [
            r'\d{1,2}[.:]\d{2}[.:]\d{2}',  # HH:MM:SS or HH.MM.SS
            r'\d{1,2}[.:]\d{2}',  # HH:MM or HH.MM
        ]
        
        for pattern in date_patterns:
            # Remove the date pattern and any surrounding spaces or underscores
            filename = re.sub(r'[\s_]*' + pattern + r'[\s_]*', '', filename)
        
        for pattern in time_patterns:
            # Remove the time pattern and any surrounding spaces or underscores
            filename = re.sub(r'[\s_]*' + pattern + r'[\s_]*', '', filename)
        
        # Clean up any double spaces that might have been left
        filename = re.sub(r'\s+', ' ', filename)  # Replace multiple spaces with single space
        filename = filename.strip(' ')  # Remove leading/trailing spaces
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Remove leading underscore if present
        filename = filename.lstrip('_')
        
        # Create new filename with standardized date format
        if has_time:
            new_filename = f"{new_datetime.strftime('%Y-%m-%d_%H-%M-%S')}_{filename}"
        else:
            new_filename = f"{new_datetime.strftime('%Y-%m-%d')}_{filename}"
        
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
    
    # Print summary
    console.print("\nSummary:", style="bold")
    console.print(f"Files already in correct format: {already_correct}", style="blue")
    console.print(f"Files renamed: {renamed_count}", style="green")
    console.print(f"Files skipped: {skipped_count}", style="yellow")
    console.print(f"Total files processed: {len(matching_files)}", style="bold")

if __name__ == "__main__":
    app()
