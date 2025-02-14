import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from sms_notifier import send_sms
from monitoring.logs.logger import Logger # type: ignore

class AlertManager:
    def __init__(self, config_path="monitoring/alert_rules.json"):
        """
        Initialize the AlertManager with the given configuration file.
        """
        self.config = self.load_config(config_path)
        self.logger = Logger("monitoring/logs/alert_manager.log")
    
    def load_config(self, path):
        """
        Load alert rules from a JSON file.
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Configuration file {path} not found.")
        with open(path, "r") as file:
            return json.load(file)
    
    def check_thresholds(self, metric, value):
        """
        Check if a given metric exceeds warning or critical thresholds.
        """
        thresholds = self.config["thresholds"].get(metric, {})
        warning = thresholds.get("warning")
        critical = thresholds.get("critical")
        
        if critical is not None and value >= critical:
            return "critical"
        elif warning is not None and value >= warning:
            return "warning"
        return "normal"
    
    def send_email(self, subject, body):
        """
        Send an alert email.
        """
        email_config = self.config["email"]
        if not email_config.get("enabled", False):
            self.logger.log("Email alerts are disabled.")
            return
        
        msg = MIMEMultipart()
        msg["From"] = email_config["username"]
        msg["To"] = ", ".join(email_config["recipients"])
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))
        
        try:
            with smtplib.SMTP(email_config["smtp_server"], email_config["port"]) as server:
                server.starttls()
                server.login(email_config["username"], email_config["password"])
                server.sendmail(email_config["username"], email_config["recipients"], msg.as_string())
                self.logger.log(f"Email alert sent: {subject}")
        except Exception as e:
            self.logger.log(f"Failed to send email: {e}", level="ERROR")
    
    def send_sms_alert(self, message):
        """
        Send an SMS alert.
        """
        sms_config = self.config["sms"]
        if not sms_config.get("enabled", False):
            self.logger.log("SMS alerts are disabled.")
            return
        
        for recipient in sms_config["recipients"]:
            try:
                send_sms(recipient, message, sms_config["gateway_url"], sms_config["api_key"])
                self.logger.log(f"SMS alert sent to {recipient}: {message}")
            except Exception as e:
                self.logger.log(f"Failed to send SMS to {recipient}: {e}", level="ERROR")
    
    def monitor_metrics(self):
        """
        Simulate monitoring system metrics and triggering alerts.
        """
        mock_metrics = {
            "cpu_usage": 85,  # Mock value for demonstration
            "memory_usage": 65,
            "network_latency": 120
        }
        
        for metric, value in mock_metrics.items():
            status = self.check_thresholds(metric, value)
            if status == "warning":
                self.logger.log(f"Warning: {metric} at {value}% exceeds warning threshold.")
                self.send_email(
                    subject=f"Warning: {metric} High",
                    body=f"<p>{metric} has reached {value}%.</p><p>Warning threshold exceeded.</p>"
                )
            elif status == "critical":
                self.logger.log(f"Critical: {metric} at {value}% exceeds critical threshold.")
                self.send_email(
                    subject=f"Critical: {metric} High",
                    body=f"<p>{metric} has reached {value}%.</p><p>Critical threshold exceeded!</p>"
                )
                self.send_sms_alert(f"Critical Alert: {metric} at {value}% exceeds critical threshold!")
    
    def run(self):
        """
        Run the alert manager at regular intervals.
        """
        interval = self.config.get("monitoring_interval_seconds", 60)
        self.logger.log("Starting AlertManager...")
        while True:
            self.monitor_metrics()
            time.sleep(interval)

if __name__ == "__main__":
    alert_manager = AlertManager()
    alert_manager.run()
