import PyPDF2
from pathlib import Path
from utils import FileLogger


# Initialize logger
logger = FileLogger("pdf_extractor")


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text content from a PDF file."""
    try:
        logger.debug(f"Opening PDF file: {pdf_path}")
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            logger.debug(f"PDF has {len(reader.pages)} pages")

            text = ""
            for i, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text += page_text
                logger.debug(f"Extracted {len(page_text)} characters from page {i}")

            logger.debug(f"Total text extracted: {len(text)} characters")
            return text
    except Exception as e:
        logger.error(f"Error reading PDF {pdf_path}: {str(e)}")
        raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")
