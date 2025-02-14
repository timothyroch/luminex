import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    """Centralized logging system for blockchain components."""

    def __init__(self, log_dir="logs", log_file="blockchain.log", level=logging.INFO, max_bytes=5 * 1024 * 1024, backup_count=5):
        """
        Initializes the logger with specified settings.
        :param log_dir: Directory to store log files.
        :param log_file: Name of the main log file.
        :param level: Logging level (default: INFO).
        :param max_bytes: Maximum size of a log file before rotation (default: 5MB).
        :param backup_count: Number of backup log files to keep (default: 5).
        """
        self.log_dir = log_dir
        self.log_file = log_file
        self.level = level
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up the logger
        self.logger = logging.getLogger("BlockchainLogger")
        self.logger.setLevel(self.level)
        self._setup_handlers()

    def _setup_handlers(self):
        """
        Sets up file and console handlers for logging.
        """
        log_path = os.path.join(self.log_dir, self.log_file)

        # File handler with log rotation
        file_handler = RotatingFileHandler(log_path, maxBytes=self.max_bytes, backupCount=self.backup_count)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self._get_formatter())

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self._get_formatter())

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _get_formatter(self):
        """
        Returns a formatter for log messages.
        :return: A logging.Formatter instance.
        """
        return logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def log(self, level, message):
        """
        Logs a message at the specified level.
        :param level: Logging level (e.g., INFO, ERROR).
        :param message: The message to log.
        """
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
        else:
            self.logger.info(message)

    def debug(self, message):
        """Logs a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Logs an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Logs an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Logs a critical message."""
        self.logger.critical(message)


# Example usage
if __name__ == "__main__":
    logger = Logger()

    logger.debug("This is a debug message.")
    logger.info("Blockchain initialized successfully.")
    logger.warning("Network latency detected.")
    logger.error("Failed to validate block #102.")
    logger.critical("Consensus failure detected!")
