import logging
import os
from transformers import pipeline, Pipeline
from typing import Dict

class ModelManager:
    """
    Gère le cycle de vie des pipelines Hugging Face.
    Les modèles sont chargés une seule fois (lazy loading) et mis en cache.
    """
    def __init__(self):
        self._pipelines: Dict[str, Pipeline] = {}
        self.config = None
        logging.info("ModelManager initialisé. Les modèles seront chargés à la demande.")

    def init_app(self, app_config):
        """Lie la configuration à l'instance du ModelManager."""
        self.config = app_config

    def _load_pipeline(self, task: str, model_name: str) -> Pipeline:
        """Charge un pipeline s'il n'est pas déjà en mémoire."""
        if task not in self._pipelines:
            logging.info(f"Chargement du modèle pour la tâche '{task}': {model_name}...")
            try:
                # Ajout pour désactiver la vérification SSL (uniquement pour le développement)
                os.environ['CURL_CA_BUNDLE'] = ''
                
                # Utilise le device spécifié dans la configuration
                device = self.config['PIPELINE_DEVICE']
                self._pipelines[task] = pipeline(task, model=model_name, device=device)
                logging.info(f"Modèle '{model_name}' chargé avec succès sur le device '{device}'.")
            except Exception as e:
                logging.error(f"Erreur lors du chargement du modèle '{model_name}': {e}")
                raise
            finally:
                # Rétablir la configuration SSL par défaut si nécessaire
                os.environ.pop('CURL_CA_BUNDLE', None)
        return self._pipelines[task]

    def get_sentiment_pipeline(self) -> Pipeline:
        return self._load_pipeline("sentiment-analysis", self.config['SENTIMENT_MODEL'])

    def get_qa_pipeline(self) -> Pipeline:
        return self._load_pipeline("question-answering", self.config['QA_MODEL'])

    def get_generation_pipeline(self) -> Pipeline:
        return self._load_pipeline("text-generation", self.config['GENERATION_MODEL'])

# Instance unique du manager, qui sera initialisée dans l'app factory.
# C'est une sorte de Singleton géré au niveau du module.
model_manager = ModelManager() 