from pathlib import Path
from datetime import datetime
from rich.console import Console
from .extract_text_from_pdf import extract_text_from_pdf
from .get_date_from_text import get_date_from_text


def get_date_from_pdf(pdf_path: Path, console: Console) -> datetime | None:
    """Main function to find a date in a PDF file."""
    try:
        console.print(f"Processing PDF: {pdf_path}", style="bright_blue")
        text: str = extract_text_from_pdf(pdf_path, console)
        # Skip if no text was extracted
        if len(text) == 0:
            console.print(
                "No text content found in PDF, skipping OpenAI request", style="yellow"
            )
            return None
        return get_date_from_text(text, console)
    except Exception as e:
        console.print(f"Error processing PDF {pdf_path}: {str(e)}", style="red")
        raise Exception(f"Error processing PDF {pdf_path}: {str(e)}")
