# Cybersecurity Monitoring and Alert System

An automated cybersecurity monitoring system that collects, analyzes, and notifies about threats in real time, helping organizations stay proactive in protecting their infrastructure.

---

## Table of Contents

- [About](#about)  
- [Features](#features)  
- [Configuration](#configuration)  
- [Installation and Usage](#installation-and-usage)  


---

## About

This system provides real-time monitoring of cybersecurity threats by integrating multiple sources of threat intelligence. Alerts are analyzed for relevance and severity, stored, and sent through multiple notification channels (Email, Slack, Telegram).  

It is designed for security teams, SOC analysts, and developers who want automated threat intelligence without manual monitoring.

---

## Features

### Data Collection
- Retrieves **CVEs** from the [NVD API](https://nvd.nist.gov/developers).  
- Scrapes **OWASP Top 10** vulnerabilities.  
- Monitors cybersecurity blogs such as [The Hacker News](https://thehackernews.com/).  

### Security Analysis
- Uses **spaCy** for NLP and entity recognition.  
- Uses **scikit-learn** (logistic regression) for threat classification.  

### Relevance Detection
- Configurable keyword-based filtering.  
- Enhanced with a **machine learning model** for higher accuracy.  

### Severity Analysis
- Classifies alerts as **Low**, **Medium**, or **High**.  

### Storage
- Stores relevant alerts in a **SQLite** database.  

### Multi-channel Notifications
- Supports **Email**, **Slack**, and **Telegram** alerts.  

---

## Configuration

Sensitive configuration values (API keys, email credentials, tokens) are managed in a `.env` file.  

Create a `.env` file in the project root with the following variables:

```env
EMAIL_USER="your_email@example.com"
EMAIL_PASS="your_password"
SLACK_TOKEN="your_slack_token"
TELEGRAM_TOKEN="your_telegram_token"
```

## Installation and Usage

### Option 1: Direct Integration

1. **Install Python on your server:**
2. **Copy all files into a /security-monitor folder**
3. **Install dependencies** :
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the .env** file with your settings
5. **Run the bot in the background:** :
   ```bash
   nohup python main.py &
   ```

### Option 2: API

1. **Use the provided `api.py`** file
2. **Install FastAPI:** :
   ```bash
   pip install fastapi uvicorn
   ```
3. **Start the API server** :
   ```bash
   uvicorn api:app --reload
   ```
4. **Connect your website**  using AJAX requests:
   ```javascript
   fetch('http://localhost:8000/alerts')
       .then(response => response.json())
       .then(data => displayAlerts(data));
   ```

## Project Structure

```
security-monitor/
├── main.py # Script principal
├── api.py # API FastAPI (optionnel)
├── requirements.txt # Liste des dépendances
├── .env # Configuration (à créer)
├── database.db # Base de données SQLite (généré automatiquement)
└── README.md # Ce fichier
