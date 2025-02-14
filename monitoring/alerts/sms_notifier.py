import requests # type: ignore
import json
from pathlib import Path
import logging

class SMSNotifier:
    def __init__(self, config_path="monitoring/alerts/alert_rules.json"):
        """
        Initialize the SMSNotifier with configuration.
        """
        self.config = self.load_config(config_path)
        self.sms_config = self.config.get("sms", {})
        self.logger = logging.getLogger("SMSNotifier")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def load_config(self, path):
        """
        Load the SMS configuration from a JSON file.
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Configuration file {path} not found.")
        with open(path, "r") as file:
            return json.load(file)

    def send_sms(self, recipient, message):
        """
        Send an SMS alert to a recipient using the SMS gateway.
        """
        if not self.sms_config.get("enabled", False):
            self.logger.warning("SMS alerts are disabled in the configuration.")
            return

        gateway_url = self.sms_config.get("gateway_url")
        api_key = self.sms_config.get("api_key")

        if not gateway_url or not api_key:
            self.logger.error("SMS gateway URL or API key is missing in the configuration.")
            return

        payload = {
            "to": recipient,
            "message": message,
            "api_key": api_key
        }

        try:
            response = requests.post(gateway_url, json=payload)
            if response.status_code == 200:
                self.logger.info(f"SMS alert sent to {recipient}: {message}")
            else:
                self.logger.error(f"Failed to send SMS to {recipient}. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.logger.error(f"Error while sending SMS to {recipient}: {e}")

if __name__ == "__main__":
    # Example usage
    notifier = SMSNotifier()
    notifier.send_sms(
        recipient="+1234567890",
        message="Critical Alert: Node 1 is down. Immediate action required."
    )
