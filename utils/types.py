from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from enum import Enum, auto


class FileType(Enum):
    """Types of files that can be processed for dates."""

    REGULAR = auto()  # Regular file with or without date
    PDF = auto()  # PDF file that might need date extraction
    # Add more file types here as needed


@dataclass
class File:
    """Represents a file that might have a date in its filename or need date extraction."""

    path: Path
    file_type: FileType
    date: datetime | None = None
    has_time: bool = False
