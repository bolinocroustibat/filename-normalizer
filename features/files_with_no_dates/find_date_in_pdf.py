from pathlib import Path
from datetime import datetime
from rich.console import Console
from .extract_text_from_pdf import extract_text_from_pdf
from .analyze_pdf_content import analyze_pdf_content


def find_date_in_pdf(pdf_path: Path, console: Console) -> datetime | None:
    """Main function to find a date in a PDF file."""
    try:
        console.print(f"Processing PDF: {pdf_path}", style="bright_blue")
        text: str = extract_text_from_pdf(pdf_path, console)
        return analyze_pdf_content(text, console)
    except Exception as e:
        console.print(f"Error processing PDF {pdf_path}: {str(e)}", style="red")
        raise Exception(f"Error processing PDF {pdf_path}: {str(e)}")
