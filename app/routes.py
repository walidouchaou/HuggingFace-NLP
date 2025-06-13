import logging
from flask import Blueprint, request, jsonify
from .services import model_manager

# Création d'un Blueprint pour regrouper les routes de l'API
# Le premier Blueprint gère les routes de prédiction
api_blueprint = Blueprint('api', __name__, url_prefix='/predict')

# Création d'un second Blueprint pour les routes générales comme la racine
general_blueprint = Blueprint('general', __name__)

@general_blueprint.route("/", methods=["GET"])
def index():
    """Route racine pour accueillir et guider l'utilisateur."""
    return jsonify({
        "message": "Bienvenue sur l'API de modèles NLP.",
        "endpoints": {
            "sentiment_analysis": "POST /predict/sentiment",
            "question_answering": "POST /predict/qa",
            "text_generation": "POST /predict/generate"
        }
    })

@general_blueprint.route('/favicon.ico')
def favicon():
    """Fournit une réponse vide pour l'icône de navigateur afin d'éviter les erreurs 404."""
    return '', 204

@api_blueprint.route("/sentiment", methods=["POST"])
def predict_sentiment():
    """Endpoint pour l'analyse de sentiment."""
    json_data = request.get_json()
    if not json_data or "text" not in json_data:
        return jsonify({"error": "Données invalides. Le champ 'text' est requis."}), 400

    text = json_data["text"]
    try:
        sentiment_pipeline = model_manager.get_sentiment_pipeline()
        results = sentiment_pipeline(text)
        # Formate la sortie comme un dictionnaire de scores {label: score}
        prediction = {res['label']: res['score'] for res in results}
        return jsonify({"prediction": prediction})
    except Exception as e:
        logging.error(f"Erreur d'inférence (sentiment): {e}")
        return jsonify({"error": "Erreur interne du serveur lors de l'analyse."}), 500


@api_blueprint.route("/qa", methods=["POST"])
def predict_qa():
    """Endpoint pour le question-réponse."""
    json_data = request.get_json()
    if not json_data or "context" not in json_data or "question" not in json_data:
        return jsonify({"error": "Données invalides. Les champs 'context' et 'question' sont requis."}), 400

    context = json_data["context"]
    question = json_data["question"]
    try:
        qa_pipeline = model_manager.get_qa_pipeline()
        result = qa_pipeline(question=question, context=context)
        return jsonify({"answer": result.get("answer", "Réponse non trouvée.")})
    except Exception as e:
        logging.error(f"Erreur d'inférence (QA): {e}")
        return jsonify({"error": "Erreur interne du serveur lors de la recherche de réponse."}), 500


@api_blueprint.route("/generate", methods=["POST"])
def predict_generate():
    """Endpoint pour la génération de texte."""
    json_data = request.get_json()
    if not json_data or "prompt" not in json_data:
        return jsonify({"error": "Données invalides. Le champ 'prompt' est requis."}), 400

    prompt = json_data["prompt"]
    max_length = json_data.get("max_length", 50)
    temperature = json_data.get("temperature", 0.9)
    try:
        generation_pipeline = model_manager.get_generation_pipeline()
        result = generation_pipeline(prompt, max_length=max_length, temperature=temperature, num_return_sequences=1)
        return jsonify({"generated_text": result[0]["generated_text"]})
    except Exception as e:
        logging.error(f"Erreur d'inférence (génération): {e}")
        return jsonify({"error": "Erreur interne du serveur lors de la génération de texte."}), 500 