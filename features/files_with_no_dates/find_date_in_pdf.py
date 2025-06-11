from pathlib import Path
from datetime import datetime
from utils import FileLogger
from .extract_text_from_pdf import extract_text_from_pdf
from .analyze_pdf_content import analyze_pdf_content


# Initialize logger
logger = FileLogger("pdf_finder")


def find_date_in_pdf(pdf_path: Path) -> datetime | None:
    """Main function to find a date in a PDF file."""
    try:
        logger.info(f"Processing PDF: {pdf_path}")
        text: str = extract_text_from_pdf(pdf_path)
        logger.debug(f"Extracted {len(text)} characters from PDF")
        return analyze_pdf_content(text)
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
        raise Exception(f"Error processing PDF {pdf_path}: {str(e)}")
