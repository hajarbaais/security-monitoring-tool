Système de Surveillance et d'Alerte de Cybersécurité
    Ce projet est un système de surveillance automatisé conçu pour collecter, analyser et notifier les menaces de cybersécurité.

    Fonctionnalités
Collecte de Données : Le système récupère des informations depuis l'API NVD pour les CVEs, effectue du scraping du Top 10 OWASP, et surveille des blogs de cybersécurité comme The Hacker News.

Analyse de Sécurité : Il utilise la bibliothèque spaCy pour l'analyse NLP et la reconnaissance d'entités.

Détection de Pertinence : La pertinence des alertes est déterminée par la présence de mots-clés configurés et par un modèle de machine learning de régression logistique.

Analyse de Sévérité : Il évalue la gravité des alertes (faible, moyenne, élevée) en fonction du contenu de l'alerte.

Stockage : Les alertes pertinentes sont stockées dans une base de données SQLite.

Notification Multi-canal : Le système peut envoyer des alertes via Email, Slack et Telegram.

    Configuration et Prérequis
Le projet s'appuie sur un fichier .env pour la configuration des paramètres sensibles et des connexions externes.
Fichier .env
Créez un fichier .env à la racine du projet avec les variables suivantes. Assurez-vous de remplacer les valeurs entre guillemets par vos propres informations (adresses email, mots de passe, tokens d'API, etc.) pour que les notifications fonctionnent correctement.


    Dépendances
Le projet utilise plusieurs bibliothèques Python. Les principales incluent :

requests

BeautifulSoup

spacy

scikit-learn

sqlite3

slack_sdk

python-telegram-bot (telegram)

python-dotenv



    Installation et Utilisation:
       Option 1: Intégration directe :
               1-Installez Python sur votre serveur

               2-Copiez tous les fichiers dans un dossier /security-monitor

               3-Installez les dépendances : pip install -r requirements.txt

               4-Lancez le bot en arrière-plan : nohup python main.py &
    
       Option 2: API :
               1-Utilisez le fichier api.py que je vous ai fourni

               2-Installez FastAPI : pip install fastapi uvicorn

               3-Lancez le serveur API :  uvicorn api:app --reload

               4-Connectez votre site avec des requêtes AJAX :fetch('http://localhost:8000/alerts')
                                                              .then(response => response.json())
                                                            .then(data => displayAlerts(data));
