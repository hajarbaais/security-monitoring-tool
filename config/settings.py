import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

      NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/1.0"
      DB_PATH = os.getenv("DB_PATH", "alerts.db")
      KEYWORDS = os.getenv("KEYWORDS", "Apache,Nginx,Linux").split(",")
    # Notification Settings
      NOTIFICATION_SETTINGS = {
        # Email
        "EMAIL_RECIPIENTS": os.getenv("EMAIL_RECIPIENTS", "admin@example.com").split(","),
        "EMAIL_SENDER": os.getenv("EMAIL_SENDER", "security-bot@example.com"),
        "EMAIL_SENDER_NAME": os.getenv("EMAIL_SENDER_NAME", "Security Alert Bot"),
        
        # Slack
        "SLACK_CHANNEL": os.getenv("SLACK_CHANNEL", "#security-alerts"),
        "SLACK_BOT_NAME": os.getenv("SLACK_BOT_NAME", "Security Alert"),
        
        # Telegram
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID", "")
    }

    # SMTP Configuration
      SMTP_CONFIG = {
        "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", 587)),
        "use_tls": os.getenv("SMTP_USE_TLS", "True") == "True"
    }

settings = Settings()