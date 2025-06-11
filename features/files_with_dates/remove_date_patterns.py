import re


def remove_date_patterns_from_filename(filename: str) -> str:
    """Remove date and time patterns from filename and clean it up."""
    # Remove date patterns
    date_patterns = [
        r"\d{4}[-_]\d{2}[-_]\d{2}",  # YYYY-MM-DD or YYYY_MM_DD
        r"\d{2}[-_]\d{2}[-_]\d{4}",  # DD-MM-YYYY or DD_MM_YYYY
        r"\d{2}[-_]\d{2}[-_]\d{2}",  # DD-MM-YY or DD_MM_YY
        r"\d{1,2}[-_]\d{1,2}[-_]\d{4}",  # M-D-YYYY or M_D_YYYY
        r"\d{1,2}[-_]\d{1,2}[-_]\d{2}",  # M-D-YY or M_D_YY
    ]

    # Remove time patterns
    time_patterns = [
        r"\d{1,2}[.:]\d{2}[.:]\d{2}",  # HH:MM:SS or HH.MM.SS
        r"\d{1,2}[.:]\d{2}",  # HH:MM or HH.MM
    ]

    for pattern in date_patterns:
        # Remove the date pattern and any surrounding spaces or underscores
        filename = re.sub(r"[\s_]*" + pattern + r"[\s_]*", "", filename)

    for pattern in time_patterns:
        # Remove the time pattern and any surrounding spaces or underscores
        filename = re.sub(r"[\s_]*" + pattern + r"[\s_]*", "", filename)

    # Clean up any double spaces that might have been left
    filename = re.sub(
        r"\s+", " ", filename
    )  # Replace multiple spaces with single space
    filename = filename.strip(" ")  # Remove leading/trailing spaces

    # Replace spaces with underscores
    filename = filename.replace(" ", "_")

    # Remove leading underscore if present
    filename = filename.lstrip("_")

    return filename
