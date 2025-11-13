from pathlib import Path
from datetime import datetime
import openai
import os
import time
from rich.console import Console


# Get OpenAI configuration from environment variables
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_date_from_pdf_with_openai(pdf_path: Path, console: Console) -> datetime | None:
    """Send PDF file directly to OpenAI to extract date when PyPDF2 fails.

    This function uploads the PDF file to OpenAI and uses the Chat Completions API
    with file attachments to extract the date from the document content.
    """
    try:
        if not OPENAI_API_KEY:
            console.print("OPENAI_API_KEY environment variable is not set", style="red")
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        if not OPENAI_API_MODEL:
            console.print("OPENAI_API_MODEL environment variable is not set", style="red")
            raise ValueError("OPENAI_API_MODEL environment variable is not set")

        console.print(
            f"Uploading PDF to OpenAI for processing: {pdf_path}", style="bright_blue"
        )
        console.print(f"Using OpenAI model: {OPENAI_API_MODEL}", style="dim")
        openai.api_key = OPENAI_API_KEY

        # Upload the PDF file to OpenAI
        with open(pdf_path, "rb") as pdf_file:
            uploaded_file = openai.files.create(file=pdf_file, purpose="assistants")

        try:
            # Wait for file to be processed
            console.print("Waiting for file to be processed...", style="dim")
            wait_count = 0
            while uploaded_file.status != "processed":
                if uploaded_file.status == "error":
                    raise Exception("File upload failed")
                wait_count += 1
                if wait_count % 5 == 0:  # Log every 5 seconds
                    console.print(f"File status: {uploaded_file.status} (waiting {wait_count}s)...", style="dim")
                time.sleep(1)
                uploaded_file = openai.files.retrieve(uploaded_file.id)
            console.print(f"File processed successfully (took {wait_count}s)", style="green")

            # Use Chat Completions API with file attachment
            console.print("Processing PDF with OpenAI Chat Completions...", style="dim")
            response = openai.chat.completions.create(
                model=OPENAI_API_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a date extraction assistant. Your task is to:
1. Analyze the PDF document content
2. Find the most relevant date that could be used for the document
3. Return ONLY the date in YYYY-MM-DD format
4. If no clear date is found, return 'NO_DATE_FOUND'
5. If multiple dates are found, return the most relevant one (usually the most recent or the document's date)
6. Do not include any explanation, just the date or NO_DATE_FOUND""",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please extract the date from this PDF document.",
                            },
                            {
                                "type": "file",
                                "file_id": uploaded_file.id,
                            },
                        ],
                    },
                ],
                temperature=0.1,
            )

            result = response.choices[0].message.content.strip()

            if result == "NO_DATE_FOUND":
                console.print("No date found in the PDF document", style="yellow")
                return None

            try:
                date = datetime.strptime(result, "%Y-%m-%d")
                console.print(
                    f"Successfully extracted date from PDF: {date.strftime('%Y-%m-%d')}",
                    style="green",
                )
                return date
            except ValueError as e:
                console.print(
                    f"Failed to parse date '{result}': {str(e)}", style="red"
                )
                return None
        finally:
            # Clean up: delete the uploaded file
            try:
                openai.files.delete(uploaded_file.id)
                console.print("Cleaned up uploaded file", style="dim")
            except Exception as cleanup_error:
                console.print(
                    f"Warning: Could not delete uploaded file: {str(cleanup_error)}",
                    style="yellow",
                )

    except Exception as e:
        console.print(f"Error processing PDF with OpenAI: {str(e)}", style="red")
        raise Exception(f"Error processing PDF with OpenAI: {str(e)}")
