from datetime import datetime
import openai
import os
from rich.console import Console


# Get OpenAI configuration from environment variables
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_date_from_text_with_openai(text: str, console: Console) -> datetime | None:
    """Analyze text content using OpenAI to find relevant dates."""
    try:
        if not OPENAI_API_KEY:
            console.print("OPENAI_API_KEY environment variable is not set", style="red")
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        # console.print(f"Using OpenAI model: {OPENAI_API_MODEL}", style="bright_blue")
        openai.api_key = OPENAI_API_KEY

        response = openai.chat.completions.create(
            model=OPENAI_API_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are a date extraction assistant. Your task is to:
                1. Analyze the text content
                2. Find the most relevant date that could be used for the document
                3. Return ONLY the date in YYYY-MM-DD format
                4. If no clear date is found, return 'NO_DATE_FOUND'
                5. If multiple dates are found, return the most relevant one (usually the most recent or the document's date)
                6. Do not include any explanation, just the date or NO_DATE_FOUND""",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.1,  # Low temperature for more consistent results
        )

        result = response.choices[0].message.content.strip()

        if result == "NO_DATE_FOUND":
            console.print("No date found in the text content", style="yellow")
            return None

        try:
            date = datetime.strptime(result, "%Y-%m-%d")
            console.print(
                f"Successfully parsed date: {date.strftime('%Y-%m-%d')}", style="green"
            )
            return date
        except ValueError as e:
            console.print(f"Failed to parse date '{result}': {str(e)}", style="red")
            return None

    except Exception as e:
        console.print(f"Error analyzing PDF content: {str(e)}", style="red")
        raise Exception(f"Error analyzing PDF content: {str(e)}")
