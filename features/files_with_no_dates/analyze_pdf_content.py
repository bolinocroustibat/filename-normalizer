from datetime import datetime
import openai
import os
from utils import FileLogger


# Get OpenAI configuration from environment variables
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", "gpt-4-turbo-preview")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize logger
logger = FileLogger("pdf_analyzer")


def analyze_pdf_content(text: str) -> datetime | None:
    """Analyze PDF content using OpenAI to find relevant dates."""
    try:
        if not OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY environment variable is not set")
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        logger.debug(f"Text length: {len(text)} characters")
        
        # Skip if no text was extracted
        if len(text) == 0:
            logger.info("No text content found in PDF, skipping OpenAI request")
            return None

        logger.debug(f"Using OpenAI model: {OPENAI_API_MODEL}")
        openai.api_key = OPENAI_API_KEY

        logger.debug("Sending text to OpenAI for date extraction")
        logger.debug(f"Text preview: {text[:200]}...")  # Show first 200 chars

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
        logger.debug(f"OpenAI response: {result}")

        if result == "NO_DATE_FOUND":
            logger.info("No date found in the text content")
            return None

        try:
            date = datetime.strptime(result, "%Y-%m-%d")
            logger.success(f"Successfully parsed date: {date.strftime('%Y-%m-%d')}")
            return date
        except ValueError as e:
            logger.error(f"Failed to parse date '{result}': {str(e)}")
            return None

    except Exception as e:
        logger.error(f"Error analyzing PDF content: {str(e)}")
        raise Exception(f"Error analyzing PDF content: {str(e)}")
