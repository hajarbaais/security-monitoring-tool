import time
import logging
from concurrent.futures import ThreadPoolExecutor
from core.collector import DataCollector
from core.analyzer import SecurityAnalyzer
from core.database import DatabaseManager
from core.notifier import NotificationSystem
from config.settings import settings

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SecurityMonitor:
    def __init__(self):
        self.collector = DataCollector()
        self.analyzer = SecurityAnalyzer()
        self.db = DatabaseManager()
        self.notifier = NotificationSystem()
        self.logger = logging.getLogger("monitor")

    def run(self):
        """Boucle principale de surveillance"""
        with ThreadPoolExecutor(max_workers=3) as executor:
            while True:
                try:
                    # Collecte parallèle
                    future_cve = executor.submit(self.collector.fetch_cves)
                    future_owasp = executor.submit(self.collector.scrape_owasp)
                    future_blog = executor.submit(self.collector.fetch_blog_updates)
                    
                    # Traitement des résultats
                    self._process_alerts(future_cve.result(), "NVD")
                    self._process_alerts(future_owasp.result(), "OWASP")
                    self._process_alerts(future_blog.result(), "Blog")
                    
                    # Pause entre les cycles
                    time.sleep(3600)  # Toutes les heures
                    
                except Exception as e:
                    self.logger.error(f"Erreur critique: {e}")
                    time.sleep(300)  

    def _process_alerts(self, alerts, source):
        """Traite une liste d'alertes"""
        for alert in alerts:
            try:
                alert["source"] = source
                analysis = self.analyzer.analyze(alert["content"])
                
                alert.update({
                    "technologies": list(analysis["technologies"]),
                    "severity": analysis["severity"],
                    "is_relevant": self.analyzer.is_relevant(alert["content"])
                })
                
                if alert["is_relevant"] and self.db.save_alert(alert):
                    self.notifier.send(alert)
                    
            except Exception as e:
                self.logger.error(f"Erreur traitement alerte: {e}")

if __name__ == "__main__":
    monitor = SecurityMonitor()
    monitor.run()