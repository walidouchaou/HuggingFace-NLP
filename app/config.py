import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir d'un fichier .env
# Utile pour le développement local
load_dotenv()

class Config:
    """
    Configuration de base de l'application.
    Charge les valeurs à partir des variables d'environnement avec des valeurs par défaut.
    """
    # Modèles Hugging Face
    SENTIMENT_MODEL = os.environ.get("SENTIMENT_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")
    QA_MODEL = os.environ.get("QA_MODEL", "distilroberta-base-squad-v2")
    GENERATION_MODEL = os.environ.get("GENERATION_MODEL", "gpt2")

    # Configuration du device pour les pipelines (ex: 'cuda:0' pour GPU, 'cpu' pour CPU)
    # L'ancien 'device=-1' est équivalent à 'cpu'.
    PIPELINE_DEVICE = os.environ.get("PIPELINE_DEVICE", "cpu") 