import re
from datetime import datetime


def parse_datetime_from_filename(filename: str) -> tuple[datetime, bool] | None:
    """Parse a datetime from a filename string.

    This function attempts to extract a date and optionally time from a filename using
    various common date and time patterns. It supports multiple date formats including
    YYYY-MM-DD, DD-MM-YYYY, DD-MM-YY, M-D-YYYY, and M-D-YY, as well as time formats
    HH:MM:SS, HH.MM.SS, HH-MM-SS, HH_MM_SS, HH:MM, HH.MM, HH-MM, and HH_MM.

    Args:
        filename (str): The filename to parse for date and time information.

    Returns:
        tuple[datetime, bool] | None: If a valid date is found, returns a tuple containing:
            - datetime: The parsed datetime object
            - bool: True if time was found, False if only date was found
        Returns None if no valid date pattern is found in the filename.
    """
    # Common date patterns in filenames
    date_patterns = [
        r"(\d{4})[-_](\d{2})[-_](\d{2})",  # YYYY-MM-DD or YYYY_MM_DD
        r"(\d{2})[-_](\d{2})[-_](\d{4})",  # DD-MM-YYYY or DD_MM_YYYY
        r"(\d{2})[-_](\d{2})[-_](\d{2})",  # DD-MM-YY or DD_MM_YY
        r"(\d{1,2})[-_](\d{1,2})[-_](\d{4})",  # M-D-YYYY or M_D_YYYY
        r"(\d{1,2})[-_](\d{1,2})[-_](\d{2})",  # M-D-YY or M_D_YY
    ]

    # Common time patterns in filenames
    time_patterns = [
        r"(\d{1,2})[.:_-](\d{2})[.:_-](\d{2})",  # HH:MM:SS, HH.MM.SS, HH-MM-SS, HH_MM_SS
        r"(\d{1,2})[.:_-](\d{2})",  # HH:MM, HH.MM, HH-MM, HH_MM
    ]

    # Try date patterns first
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            try:
                # Handle YYYY-MM-DD format
                if len(match.group(1)) == 4:
                    year = int(match.group(1))
                    month = int(match.group(2))
                    day = int(match.group(3))
                else:
                    # Handle other formats
                    if len(match.group(3)) == 2:  # If year is 2 digits
                        year = int(match.group(3))
                        if year < 50:  # Assuming years 00-49 are 2000-2049
                            year += 2000
                        else:  # Assuming years 50-99 are 1950-1999
                            year += 1900
                    else:
                        year = int(match.group(3))

                    month = int(match.group(2))
                    day = int(match.group(1))

                # Check if there's a time pattern after the date
                time_match = None
                for time_pattern in time_patterns:
                    time_match = re.search(time_pattern, filename[match.end() :])
                    if time_match:
                        break

                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2))
                    second = (
                        int(time_match.group(3)) if len(time_match.groups()) > 2 else 0
                    )
                    return datetime(year, month, day, hour, minute, second), True
                else:
                    return datetime(year, month, day), False
            except ValueError:
                continue
    return None
