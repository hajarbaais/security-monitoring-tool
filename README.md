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

## Installation et Utilisation

### Option 1: Intégration directe

1. **Installez Python** sur votre serveur
2. **Copiez tous les fichiers** dans un dossier `/security-monitor`
3. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurez le fichier .env** avec vos paramètres
5. **Lancez le bot en arrière-plan** :
   ```bash
   nohup python main.py &
   ```

### Option 2: API

1. **Utilisez le fichier `api.py`** que je vous ai fourni
2. **Installez FastAPI** :
   ```bash
   pip install fastapi uvicorn
   ```
3. **Lancez le serveur API** :
   ```bash
   uvicorn api:app --reload
   ```
4. **Connectez votre site** avec des requêtes AJAX :
   ```javascript
   fetch('http://localhost:8000/alerts')
       .then(response => response.json())
       .then(data => displayAlerts(data));
   ```

## Structure du Projet

```
security-monitor/
├── main.py # Script principal
├── api.py # API FastAPI (optionnel)
├── requirements.txt # Liste des dépendances
├── .env # Configuration (à créer)
├── database.db # Base de données SQLite (généré automatiquement)
└── README.md # Ce fichier
