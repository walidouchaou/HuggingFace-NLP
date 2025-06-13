import logging
from flask import Flask, jsonify
from flask.json.provider import JSONProvider
import json

from app.config import Config
from app.services import model_manager
from app.routes import api_blueprint, general_blueprint

# ==============================================================================
# Amélioration pour s'assurer que l'encodage UTF-8 est bien géré
# ==============================================================================
class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        kwargs.setdefault('ensure_ascii', False)
        return json.dumps(obj, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

# ==============================================================================
# Application Factory
# ==============================================================================
def create_app():
    """
    Crée et configure une instance de l'application Flask.
    Ce pattern est idéal pour la testabilité et la modularité.
    """
    app = Flask(__name__)
    
    # 1. Configuration de l'application
    app.config.from_object(Config)
    app.json = CustomJSONProvider(app)

    # 2. Configuration du logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 3. Initialisation des services
    # Le ModelManager est initialisé ici avec la configuration de l'app.
    model_manager.init_app(app.config)

    # 4. Enregistrement des Blueprints (nos routes)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(general_blueprint)

    # 5. Gestionnaire d'erreurs global
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Gestionnaire global pour les erreurs non interceptées."""
        # Log l'exception complète pour le débogage
        logging.error(f"Une erreur non gérée est survenue: {e}", exc_info=True)
        # Retourne une réponse générique pour ne pas exposer les détails
        return jsonify(error="Une erreur interne inattendue est survenue sur le serveur."), 500

    logging.info("Application Flask créée et configurée.")
    return app 