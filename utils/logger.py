import logging
import logging.handlers
import os
from pathlib import Path
from typing import Literal
from rich.console import Console
from rich.theme import Theme
from rich.text import Text

# Define custom theme for consistent colors
rich_theme = Theme({
    "info": "bright_black",  # Subtle but visible gray
    "debug": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "path": "bright_blue",   # Brighter blue for better visibility
    "bold": "bold",
})


class FileLogger:
    """A logger that combines file and console output with rich formatting.

    This logger provides both file and console output with consistent formatting.
    It uses Rich for console output and Python's logging for file output.
    Log levels can be configured via the LOG_LEVEL environment variable.
    """

    def __init__(self, name: str = "filename_normalizer") -> None:
        """Initialize the logger with both file and console handlers.

        Args:
            name: The name of the logger, used to identify the source in logs.
        """
        # Get log level from environment variable, default to INFO
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)

        # Initialize logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Set up file handler with rotation
        log_file_path = Path("app.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3,
            encoding="UTF-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s: %(message)s",
                "%Y-%m-%d %H:%M:%S"
            )
        )
        self.logger.addHandler(file_handler)

        # Initialize Rich console with custom theme
        self.console = Console(theme=rich_theme)

    def _format_message(self, message: str) -> Text:
        """Format a message with path highlighting.

        Args:
            message: The message to format

        Returns:
            A Rich Text object with appropriate styling
        """
        text = Text(message)
        
        # Find and highlight paths
        parts = message.split(": ")
        if len(parts) > 1:
            # Style the prefix (before the path)
            text.stylize("info", 0, len(parts[0]) + 2)
            # Style the path
            text.stylize("path", len(parts[0]) + 2)
        else:
            # If no path found, style the whole message
            text.stylize("info")
            
        return text

    def _log(
        self,
        level: Literal["info", "debug", "warning", "error"],
        message: str,
        rich_style: str
    ) -> None:
        """Internal method to handle logging to both file and console.

        Args:
            level: The logging level to use
            message: The message to log
            rich_style: The Rich style to use for console output
        """
        log_method = getattr(self.logger, level)
        if self.logger.isEnabledFor(getattr(logging, level.upper())):
            # Format the message with path highlighting
            formatted_text = self._format_message(message)
            self.console.print(formatted_text)
            log_method(message)

    def info(self, message: str) -> None:
        self._log("info", message, "info")

    def debug(self, message: str) -> None:
        self._log("debug", message, "debug")

    def warning(self, message: str) -> None:
        self._log("warning", message, "warning")

    def error(self, message: str) -> None:
        self._log("error", message, "error")

    def success(self, message: str) -> None:
        self._log("info", message, "success")
