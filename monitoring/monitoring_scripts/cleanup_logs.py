import os
import time
import logging
from datetime import datetime, timedelta
import json

class LogCleanup:
    def __init__(self, config_path="monitoring/logs/monitoring_config.json"):
        """
        Initializes the LogCleanup class with configuration.
        """
        self.config = self.load_config(config_path)
        self.log_directories = self.config.get("log_directories", [])
        self.retention_days = self.config.get("retention_days", 30)
        self.logger = self.setup_logger()

    def load_config(self, path):
        """
        Loads the configuration file.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration file {path} not found.")
        with open(path, "r") as file:
            return json.load(file)

    def setup_logger(self):
        """
        Sets up the logger for the script.
        """
        logger = logging.getLogger("LogCleanup")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("cleanup_logs.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def delete_old_logs(self, directory):
        """
        Deletes log files older than the configured retention period.
        """
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        self.logger.info(f"Cleaning up logs in {directory} older than {self.retention_days} days.")

        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith(".log"):
                        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if file_mtime < cutoff_date:
                            os.remove(file_path)
                            self.logger.info(f"Deleted: {file_path}")
        except Exception as e:
            self.logger.error(f"Error while cleaning logs in {directory}: {e}")

    def run(self):
        """
        Runs the cleanup process for all specified directories.
        """
        for directory in self.log_directories:
            if os.path.exists(directory):
                self.delete_old_logs(directory)
            else:
                self.logger.warning(f"Directory {directory} does not exist.")

if __name__ == "__main__":
    # Load configuration and start the log cleanup process
    cleanup = LogCleanup()
    cleanup.run()
