from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from enum import Enum, auto


class FileType(Enum):
    """Types of files that can be processed for dates."""

    PDF = auto()
    # Add more file types here as needed


@dataclass
class FileWithDate:
    """Represents a file that has a date in its filename."""

    path: Path
    date: datetime
    has_time: bool


@dataclass
class FileWithNoDate:
    """Represents a file that doesn't have a date in its filename but might need processing."""

    path: Path
    file_type: FileType
