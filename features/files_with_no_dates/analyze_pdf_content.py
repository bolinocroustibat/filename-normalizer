from datetime import datetime
import openai
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Get OpenAI configuration from environment variables
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", "gpt-4-turbo-preview")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def analyze_pdf_content(text: str) -> datetime | None:
    """Analyze PDF content using OpenAI to find relevant dates."""
    try:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

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
            return None

        try:
            return datetime.strptime(result, "%Y-%m-%d")
        except ValueError:
            return None

    except Exception as e:
        raise Exception(f"Error analyzing PDF content: {str(e)}")
