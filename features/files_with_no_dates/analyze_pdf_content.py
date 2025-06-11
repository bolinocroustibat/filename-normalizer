from datetime import datetime
import openai
from typing import Optional
import os


# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")


def analyze_pdf_content(text: str) -> Optional[datetime]:
    """Analyze PDF content using OpenAI to find relevant dates."""
    try:
        openai.api_key = OPENAI_API_KEY

        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",  # Using the latest model for best results
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
