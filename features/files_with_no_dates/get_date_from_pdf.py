from pathlib import Path
from datetime import datetime
from rich.console import Console
from .extract_text_from_pdf_with_pypdf2 import extract_text_from_pdf_with_pypdf2
from .get_date_from_text_with_openai import get_date_from_text_with_openai
from .get_date_from_pdf_with_openai import get_date_from_pdf_with_openai


def get_date_from_pdf(pdf_path: Path, console: Console) -> datetime | None:
    """Main function to find a date in a PDF file.

    First tries to extract text using PyPDF2, then uses OpenAI to extract date from text.
    If PyPDF2 fails to extract any text, falls back to sending the PDF directly to OpenAI.
    """
    try:
        console.print(f"Processing PDF: {pdf_path}", style="bright_blue")
        text: str = extract_text_from_pdf_with_pypdf2(pdf_path, console)
        # If text was extracted successfully, use OpenAI to extract date from text
        if len(text) > 0:
            return get_date_from_text_with_openai(text, console)

        # Fallback: PyPDF2 couldn't extract text, send PDF directly to OpenAI
        console.print(
            "No text content found with PyPDF2, falling back to OpenAI PDF processing",
            style="yellow",
        )
        return get_date_from_pdf_with_openai(pdf_path, console)
    except Exception as e:
        console.print(f"Error processing PDF {pdf_path}: {str(e)}", style="red")
        raise Exception(f"Error processing PDF {pdf_path}: {str(e)}")
