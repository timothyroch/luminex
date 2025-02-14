import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import json
import logging

class EmailNotifier:
    def __init__(self, config_path="monitoring/alerts/alert_rules.json"):
        """
        Initialize the EmailNotifier with configuration.
        """
        self.config = self.load_config(config_path)
        self.email_config = self.config.get("email", {})
        self.logger = logging.getLogger("EmailNotifier")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def load_config(self, path):
        """
        Load the email configuration from a JSON file.
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Configuration file {path} not found.")
        with open(path, "r") as file:
            return json.load(file)

    def send_email(self, subject, body):
        """
        Send an email using the configuration.
        """
        if not self.email_config.get("enabled", False):
            self.logger.warning("Email alerts are disabled in the configuration.")
            return

        recipients = self.email_config.get("recipients", [])
        if not recipients:
            self.logger.error("No email recipients specified.")
            return

        msg = MIMEMultipart()
        msg["From"] = self.email_config["username"]
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(self.email_config["smtp_server"], self.email_config["port"]) as server:
                server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
                server.login(self.email_config["username"], self.email_config["password"])
                server.sendmail(self.email_config["username"], recipients, msg.as_string())
                self.logger.info(f"Email alert sent: {subject}")
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Example usage
    notifier = EmailNotifier()
    notifier.send_email(
        subject="Test Alert: High CPU Usage",
        body="<p>CPU usage has exceeded 90% on Node 1.</p><p>Please take action immediately.</p>"
    )
