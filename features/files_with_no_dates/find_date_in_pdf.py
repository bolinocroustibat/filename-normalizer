from pathlib import Path
from datetime import datetime
from .extract_text_from_pdf import extract_text_from_pdf
from .analyze_pdf_content import analyze_pdf_content


def find_date_in_pdf(pdf_path: Path) -> datetime | None:
    """Main function to find a date in a PDF file."""
    try:
        text: str = extract_text_from_pdf(pdf_path)
        return analyze_pdf_content(text)
    except Exception as e:
        raise Exception(f"Error processing PDF {pdf_path}: {str(e)}")
