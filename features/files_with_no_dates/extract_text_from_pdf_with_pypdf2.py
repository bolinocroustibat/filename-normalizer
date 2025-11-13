import PyPDF2
from pathlib import Path
import warnings
from rich.console import Console


def extract_text_from_pdf_with_pypdf2(pdf_path: Path, console: Console) -> str:
    """Extract text content from a PDF file using PyPDF2."""
    try:
        # console.print(f"Opening PDF file: {pdf_path}", style="bright_blue")
        # Suppress PyPDF2 encoding warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module="PyPDF2")
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                # console.print(f"PDF has {len(reader.pages)} pages", style="bright_blue")

                text = ""
                for i, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    text += page_text
                    # console.print(f"Extracted {len(page_text)} characters from page {i}", style="bright_blue")

                # console.print(f"Total text extracted: {len(text)} characters", style="bright_blue")
                return text
    except Exception as e:
        console.print(f"Error reading PDF {pdf_path}: {str(e)}", style="red")
        raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")
