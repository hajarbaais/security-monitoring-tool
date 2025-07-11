import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
from config.settings import settings

class DataCollector:
    @staticmethod
    def fetch_cves(days=1):
        """Récupère les CVE des dernières 24h"""
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
        
        params = {
            "pubStartDate": start_date,
            "resultsPerPage": 2000
        }
        
        try:
            response = requests.get(settings.NVD_API_URL, params=params, timeout=15)
            response.raise_for_status()
            return response.json()["result"]["CVE_Items"]
        except Exception as e:
            print(f"Erreur API NVD: {e}")
            return []

    @staticmethod
    def scrape_owasp():
        """Scrape le Top 10 OWASP"""
        try:
            response = requests.get("https://owasp.org/www-project-top-ten/", timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            return [
                {
                    "title": item.select_one('h3').text.strip(),
                    "content": item.select_one('.topten-description').text.strip(),
                    "source": "OWASP"
                }
                for item in soup.select('.topten-item')
            ]
        except Exception as e:
            print(f"Erreur scraping OWASP: {e}")
            return []

    @staticmethod
    def fetch_blog_updates():
        """Exemple pour The Hacker News"""
        try:
            response = requests.get("https://thehackernews.com/", timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            return [
                {
                    "title": article.select_one('.home-title').text.strip(),
                    "content": article.select_one('.home-desc').text.strip(),
                    "source": "The Hacker News"
                }
                for article in soup.select('.blog-post')[:10]  # Limite à 10 articles
            ]
        except Exception as e:
            print(f"Erreur scraping blog: {e}")
            return []