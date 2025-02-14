import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class TestLogger:
    LOG_DIR = "test/logs"
    LOG_FILE = "test_log.log"
    MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
    BACKUP_COUNT = 3

    @staticmethod
    def setup_logger():
        """
        Set up the test logger with a rotating file handler.
        """
        if not os.path.exists(TestLogger.LOG_DIR):
            os.makedirs(TestLogger.LOG_DIR)

        log_file_path = os.path.join(TestLogger.LOG_DIR, TestLogger.LOG_FILE)
        
        logger = logging.getLogger("TestLogger")
        logger.setLevel(logging.DEBUG)

        # File handler for log rotation
        file_handler = RotatingFileHandler(
            log_file_path, maxBytes=TestLogger.MAX_LOG_SIZE, backupCount=TestLogger.BACKUP_COUNT
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_format)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

# Create a global logger instance
logger = TestLogger.setup_logger()

if __name__ == "__main__":
    # Example usage of TestLogger
    logger.info("Test suite started")
    logger.debug("Initializing mock data for test cases")
    logger.warning("Mock data for node 3 missing, using fallback")
    logger.error("Failed to connect to RPC endpoint")
    logger.critical("Test suite aborted due to critical error")
