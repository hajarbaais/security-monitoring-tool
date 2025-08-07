import spacy
from spacy.language import Language
from spacy.matcher import PhraseMatcher, Matcher    
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from config.settings import settings

nlp = spacy.load("en_core_web_lg")

class SecurityAnalyzer:
    def __init__(self):

        self._setup_nlp()
        
       
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = LogisticRegression()
        self._train_init_model()

    def _setup_nlp(self):
        """Configure les règles de détection spécifiques"""
       
        cyber_terms = ["RCE", "XSS", "SQLi", "CVE-", "Zero-Day", "Privilege Escalation"]
        matcher = PhraseMatcher(nlp.vocab)
        matcher.add("CYBER_TERMS", [nlp(text) for text in cyber_terms])

       
        version_patterns = [
            {"label": "SOFTWARE_VERSION", "pattern": [{"TEXT": {"REGEX": r"\d+\.\d+(\.\d+)?"}}]}
        ]
        
        ruler = nlp.add_pipe("entity_ruler", before="ner")
        ruler.add_patterns(version_patterns)

       
        Language.factory("cyber_component", func=lambda nlp, name: self._cyber_component)
        nlp.add_pipe("cyber_component", after="ner")

    def _cyber_component(self, doc):
        """Composant custom pour la cybersécurité"""
        matches = self.matcher(doc)
        spans = [doc[start:end] for _, start, end in matches]
        doc.ents = list(doc.ents) + spans
        return doc

    def _train_init_model(self):
        """Entraînement initial du modèle"""
        texts = [
            "Apache HTTP Server vulnerability",
            "WordPress security update",
            "Linux kernel flaw",
            "Python Django patch"
        ]
        labels = [1, 0, 1, 0]
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def analyze(self, text):
        """Analyse complète d'un texte"""
        doc = nlp(text)
        
        results = {
            "technologies": set(),
            "versions": set(),
            "vulnerabilities": set(),
            "severity": "low"
        }

        for ent in doc.ents:
            if ent.label_ in ("ORG", "PRODUCT"):
                results["technologies"].add(ent.text)
            elif ent.label_ == "SOFTWARE_VERSION":
                results["versions"].add(ent.text)
            elif ent.label_ == "CYBER_TERMS":
                results["vulnerabilities"].add(ent.text)

        # Détection de criticité
        if any(word in text.lower() for word in ["critical", "urgent", "0-day"]):
            results["severity"] = "high"
        elif any(word in text.lower() for word in ["high", "important"]):
            results["severity"] = "medium"

        return results

    def is_relevant(self, text):
        """Détermine si le texte est pertinent"""
        analysis = self.analyze(text)
        
        # Vérification par mots-clés
        if any(keyword.lower() in text.lower() for keyword in settings.KEYWORDS):
            return True
            
        # Vérification par modèle ML
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0] == 1

    def save_model(self, path="models/relevance_model.pkl"):
        """Sauvegarde le modèle"""
        with open(path, "wb") as f:
            pickle.dump((self.vectorizer, self.model), f)

    def load_model(self, path="models/relevance_model.pkl"):
        """Charge un modèle sauvegardé"""
        with open(path, "rb") as f:
            self.vectorizer, self.model = pickle.load(f)