Cybersecurity Monitoring and Alert System

This project is an automated monitoring system designed to collect, analyze, and notify about cybersecurity threats in real time.

Features

Data Collection

Retrieves CVEs from the NVD API.

Scrapes the OWASP Top 10.

Monitors cybersecurity blogs such as The Hacker News.

Security Analysis

Uses spaCy for NLP and entity recognition.

Employs scikit-learn (logistic regression) for classification.

Relevance Detection

Based on configurable keywords.

Enhanced with a machine learning model for higher accuracy.

Severity Analysis

Classifies alerts as Low, Medium, or High.

Storage

Persists relevant alerts in a SQLite database.

Multi-channel Notifications

Supports Email, Slack, and Telegram alerts.

Configuration and Prerequisites

The project uses a .env file to manage sensitive configuration values such as API keys, email credentials, and tokens.

Create a .env file in the project root with the following variables:

EMAIL_USER="your_email@example.com"
EMAIL_PASS="your_password"
SLACK_TOKEN="your_slack_token"
TELEGRAM_TOKEN="your_telegram_token"


Important: Never share your .env file in version control systems such as GitHub.

Dependencies

This project requires the following Python libraries:

requests

beautifulsoup4

spacy

scikit-learn

sqlite3

slack_sdk

python-telegram-bot

python-dotenv

Install them using:

pip install -r requirements.txt

Installation and Usage
Option 1: Direct Integration

Install Python on your server.

Copy all project files into a directory (e.g., /security-monitor).

Install dependencies:

pip install -r requirements.txt


Run the bot in the background:

nohup python main.py &

Option 2: API Integration

Use the provided api.py file.

Install FastAPI and Uvicorn:

pip install fastapi uvicorn


Start the API server:

uvicorn api:app --reload


Connect your website using AJAX requests:

fetch('http://localhost:8000/alerts')

Roadmap

Add support for Discord notifications.

Implement advanced machine learning models for threat classification.

Develop a dashboard for real-time monitoring.

Contributing

Contributions are welcome. Please open an issue or submit a pull request to propose improvements.

License

This project is licensed under the MIT License.                                                   .then(response => response.json())
                                                            .then(data => displayAlerts(data));
