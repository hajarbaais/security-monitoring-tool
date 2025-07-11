import sqlite3
from datetime import datetime
from config.settings import settings

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(settings.DB_PATH)
        self._init_db()

    def _init_db(self):
        """Initialise la structure de la BDD"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                source TEXT,
                title TEXT,
                content TEXT,
                is_relevant BOOLEAN,
                severity TEXT,
                technologies TEXT,
                date_added TIMESTAMP
            )
        ''')
        self.conn.commit()

    def save_alert(self, alert):
        """Sauvegarde une alerte"""
        cursor = self.conn.cursor()
        
        technologies = ", ".join(alert.get("technologies", []))
        
        cursor.execute('''
            INSERT OR IGNORE INTO alerts 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert.get("id"),
            alert.get("source"),
            alert.get("title"),
            alert.get("content"),
            alert.get("is_relevant", False),
            alert.get("severity", "low"),
            technologies,
            datetime.now()
        ))
        self.conn.commit()
        return cursor.rowcount > 0  
    
    def get_recent_alerts(self, limit=10):
        """Récupère les alertes récentes"""
        cursor = self.conn.cursor()
        return cursor.execute('''
            SELECT * FROM alerts 
            ORDER BY date_added DESC 
            LIMIT ?
        ''', (limit,)).fetchall()

    def close(self):
        """Ferme la connexion"""
        self.conn.close()