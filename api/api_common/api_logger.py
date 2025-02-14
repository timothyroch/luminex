import logging
from logging.handlers import RotatingFileHandler
from flask import request # type: ignore

# Configure logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Set up rotating file handler (5 MB per file, 5 backups)
handler = RotatingFileHandler("monitoring/logs/api_logs.log", maxBytes=5 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_request():
    """Logs details of incoming API requests."""
    logger.info(
        f"REQUEST - Method: {request.method}, Path: {request.path}, IP: {request.remote_addr}, Data: {request.get_json()}"
    )

def log_response(response):
    """Logs details of outgoing API responses."""
    logger.info(
        f"RESPONSE - Status: {response.status_code}, Path: {request.path}, Data: {response.get_data(as_text=True)}"
    )
    return response

def log_error(error):
    """Logs details of errors or exceptions."""
    logger.error(f"ERROR - Path: {request.path}, Error: {str(error)}")
