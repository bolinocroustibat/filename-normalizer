import logging
import logging.handlers
import os
from pathlib import Path


class FileLogger:
    WHITE = "\033[97m"
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def __init__(self, name: str = "filename_normalizer") -> None:
        # Get log level from environment variable, default to INFO
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)

        # logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Set log file path in root directory
        log_file_path = Path("app.log")

        # handler
        five_mbytes = 10**6 * 5
        handler = logging.handlers.RotatingFileHandler(
            log_file_path, maxBytes=five_mbytes, encoding="UTF-8", backupCount=0
        )
        handler.setLevel(log_level)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        # add formatter to handler
        handler.setFormatter(formatter)

        # add handler to logger
        self.logger.addHandler(handler)

    def log(self, message: str) -> None:
        if self.logger.isEnabledFor(logging.INFO):
            print(f"{self.WHITE}{message}{self.ENDC}")
            self.logger.info(message)

    def info(self, message: str) -> None:
        if self.logger.isEnabledFor(logging.INFO):
            print(f"{self.PURPLE}{message}{self.ENDC}")
            self.logger.info(message)

    def debug(self, message: str) -> None:
        if self.logger.isEnabledFor(logging.DEBUG):
            print(f"{self.CYAN}{message}{self.ENDC}")
            self.logger.debug(message)

    def warning(self, message: str) -> None:
        if self.logger.isEnabledFor(logging.WARNING):
            print(f"{self.YELLOW}{message}{self.ENDC}")
            self.logger.warning(message)

    def error(self, message: str) -> None:
        if self.logger.isEnabledFor(logging.ERROR):
            print(f"{self.RED}{message}{self.ENDC}")
            self.logger.error(message)

    def success(self, message: str) -> None:
        if self.logger.isEnabledFor(logging.INFO):
            print(f"{self.GREEN}{message}{self.ENDC}")
            self.logger.info(message)
