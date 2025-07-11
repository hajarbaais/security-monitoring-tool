import smtplib
import os
import logging
from email.mime.text import MIMEText
from slack_sdk import WebClient
from telegram import Bot
from config.settings import settings

class NotificationSystem:
    def __init__(self):
       
        self.slack = self._init_slack()
        self.telegram = self._init_telegram()
        self.logger = logging.getLogger("notifier")
        
    def _init_slack(self):
        if "SLACK_TOKEN" in os.environ:
            try:
                return WebClient(token=os.getenv("SLACK_TOKEN"))
            except Exception as e:
                self.logger.error(f"Slack initialization failed: {e}")
        return None

    def _init_telegram(self):
        if "TELEGRAM_TOKEN" in os.environ:
            try:
                return Bot(token=os.getenv("TELEGRAM_TOKEN"))
            except Exception as e:
                self.logger.error(f"Telegram initialization failed: {e}")
        return None

    def send(self, alert, channels=None):
        """Send notification through specified channels"""
        if channels is None:
            channels = ["email"]  
        
        message = self._format_message(alert)
        recipients = settings.NOTIFICATION_SETTINGS
        
        try:
            if "slack" in channels and self.slack:
                self._send_slack(message, recipients)
            
            if "email" in channels:
                self._send_email(message, alert, recipients)
                
            if "telegram" in channels and self.telegram:
                self._send_telegram(message, recipients)
                
        except Exception as e:
            self.logger.error(f"Notification failed: {e}")

    def _format_message(self, alert):
        """Format alert message with emoji based on severity"""
        severity = alert.get("severity", "low").lower()
        emojis = {
            "critical": "🔥🔥",
            "high": "🔥", 
            "medium": "⚠️",
            "low": "ℹ️"
        }
        emoji = emojis.get(severity, "📌")
        
        return f"""
{emoji} *{alert.get('title', 'No title')}* [{severity.upper()}]
🔗 Source: {alert.get('source', 'Unknown')}
📅 Date: {alert.get('date', 'N/A')}

📝 Description:
{alert.get('content', 'No content provided')[:500]}...

🛠 Technologies: {', '.join(alert.get('technologies', ['Unknown']))}
"""

    def _send_slack(self, message, recipients):
        """Send message to Slack"""
        try:
            response = self.slack.chat_postMessage(
                channel=recipients["SLACK_CHANNEL"],
                text=message,
                username=recipients["SLACK_BOT_NAME"],
                icon_emoji=":shield:"
            )
            self.logger.info(f"Slack notification sent: {response}")
        except Exception as e:
            self.logger.error(f"Slack error: {e}")
            raise

    def _send_email(self, message, alert, recipients):
        """Send email notification"""
        try:
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = f"[{alert.get('severity', 'ALERT').upper()}] {alert.get('title', 'Security Alert')}"
            msg['From'] = f"{recipients['EMAIL_SENDER_NAME']} <{recipients['EMAIL_SENDER']}>"
            msg['To'] = ", ".join(recipients["EMAIL_RECIPIENTS"])
            
            with smtplib.SMTP(
                host=settings.SMTP_CONFIG["server"],
                port=settings.SMTP_CONFIG["port"]
            ) as server:
                if settings.SMTP_CONFIG["use_tls"]:
                    server.starttls()
                server.login(
                    recipients["EMAIL_SENDER"],
                    os.getenv("EMAIL_PASSWORD")
                )
                server.send_message(msg)
                self.logger.info("Email notification sent successfully")
        except Exception as e:
            self.logger.error(f"Email error: {e}")
            raise

    def _send_telegram(self, message, recipients):
        """Send Telegram notification"""
        try:
            self.telegram.send_message(
                chat_id=recipients["TELEGRAM_CHAT_ID"],
                text=message,
                parse_mode="Markdown"
            )
            self.logger.info("Telegram notification sent")
        except Exception as e:
            self.logger.error(f"Telegram error: {e}")
            raise

# Test function
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    test_alert = {
        "title": "TEST: Vulnerability Detected",
        "content": "This is a test notification of the security alert system.",
        "severity": "high",
        "source": "Security Bot Test Suite",
        "technologies": ["Apache", "Linux"],
        "date": "2023-11-15"
    }
    
    notifier = NotificationSystem()
    notifier.send(test_alert, channels=["email", "slack", "telegram"])