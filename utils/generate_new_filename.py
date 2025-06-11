from datetime import datetime


def generate_filename(cleaned_filename: str, datetime: datetime, has_time: bool) -> str:
    """Generate a filename with standardized date format."""
    if has_time:
        return f"{datetime.strftime('%Y-%m-%d_%H-%M-%S')}_{cleaned_filename}"
    else:
        return f"{datetime.strftime('%Y-%m-%d')}_{cleaned_filename}"
