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

        # Use Responses API with minimal reasoning and low verbosity
        response = openai.responses.create(
            model=OPENAI_API_MODEL,
            input=f"""You are a date extraction assistant. Your task is to:
1. Analyze the text content
2. Find the most relevant date that could be used for the document
3. Return ONLY the date in YYYY-MM-DD format
4. If no clear date is found, return 'NO_DATE_FOUND'
5. If multiple dates are found, return the most relevant one (usually the most recent or the document's date)
6. Do not include any explanation, just the date or NO_DATE_FOUND

Text content:
{text}""",
            reasoning={"effort": "minimal"},  # Fast and cost-effective for simple tasks
            text={"verbosity": "low"},  # We only need YYYY-MM-DD, no explanations
        )
        result = response.output[0].content if response.output else None
        if result:
            result = result.strip()

        if not result:
            console.print("No response from OpenAI", style="yellow")
            return None

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
