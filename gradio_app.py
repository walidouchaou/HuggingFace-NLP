import gradio as gr
import requests
import os

# ==============================================================================
# 1. Configuration Centralisée
# ==============================================================================
# Utilise des variables d'environnement si disponibles, sinon des valeurs par défaut.
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:5000")
REQUEST_TIMEOUT = 30 # Secondes

# ==============================================================================
# 2. Client API Dédié
# ==============================================================================
# Cette classe robuste gère la communication avec le backend Flask.
class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def _post(self, endpoint: str, json_data: dict) -> dict:
        """Méthode générique pour effectuer une requête POST et gérer les erreurs."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=json_data, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_message = e.response.json().get('error', str(e))
            raise gr.Error(f"Erreur du serveur d'API : {error_message}")
        except requests.exceptions.RequestException as e:
            raise gr.Error(f"Erreur de communication avec l'API : {e}")

    def predict_sentiment(self, text: str) -> dict:
        """Appelle le endpoint de l'analyse de sentiment."""
        response_data = self._post("/predict/sentiment", {"text": text})
        return response_data.get('prediction', {})

    def answer_question(self, context: str, question: str) -> str:
        """Appelle le endpoint de question-réponse."""
        response_data = self._post("/predict/qa", {"context": context, "question": question})
        return response_data.get('answer', "Aucune réponse reçue de l'API.")

    def generate_text(self, prompt: str, max_length: int, temperature: float) -> str:
        """Appelle le endpoint de génération de texte."""
        payload = {"prompt": prompt, "max_length": max_length, "temperature": temperature}
        response_data = self._post("/predict/generate", payload)
        return response_data.get('generated_text', "Aucun texte généré.")

# ==============================================================================
# 3. Construction de l'interface Gradio Experte
# ==============================================================================
def create_expert_ui(api_client: ApiClient):
    
    # Thème moderne et épuré
    theme = gr.themes.Default(primary_hue="blue", secondary_hue="blue", neutral_hue="slate").set(
        button_primary_background_fill='linear-gradient(90deg, #3B82F6, #1D4ED8)'
    )
    
    # CSS personnalisé pour des finitions parfaites
    custom_css = """
    .gradio-container { border-radius: 20px !important; }
    .tab-nav button { border-radius: 10px 10px 0 0 !important; }
    footer { display: none !important }
    """

    with gr.Blocks(theme=theme, css=custom_css, title="Client NLP Expert") as demo:
        gr.Markdown(
            """
            <div style="text-align: center; font-family: 'Helvetica Neue', sans-serif;">
                <h1>🚀 Interface Experte pour API NLP 🚀</h1>
                <p>Une interface réactive et robuste pour interagir avec le backend de modèles Transformers.</p>
            </div>
            """
        )

        with gr.Tabs():
            # === Onglet 1: Analyse de Sentiment ===
            with gr.TabItem("🔎 Analyse de Sentiment"):
                with gr.Row():
                    sentiment_input = gr.Textbox(lines=8, label="Texte à analyser", placeholder="Collez votre texte ici...")
                    sentiment_output = gr.Label(label="Résultat")
                sentiment_button = gr.Button("Analyser le sentiment", variant="primary")
                sentiment_button.click(
                    fn=api_client.predict_sentiment,
                    inputs=[sentiment_input],
                    outputs=[sentiment_output]
                )

            # === Onglet 2: Question-Réponse ===
            with gr.TabItem("❓ Question-Réponse"):
                qa_context = gr.Textbox(lines=10, label="Contexte", placeholder="Fournissez le contexte de référence...")
                with gr.Row():
                    qa_question = gr.Textbox(label="Question", placeholder="Posez votre question sur le contexte...")
                    qa_output = gr.Textbox(label="Réponse", interactive=False)
                qa_button = gr.Button("Trouver la réponse", variant="primary")
                qa_button.click(
                    fn=api_client.answer_question,
                    inputs=[qa_context, qa_question],
                    outputs=[qa_output]
                )

            # === Onglet 3: Génération de Texte ===
            with gr.TabItem("✍️ Génération de Texte"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gen_input = gr.Textbox(lines=5, label="Amorce (Prompt)", placeholder="Écrivez le début du texte à générer...")
                        with gr.Accordion("Paramètres avancés", open=False):
                            gen_max_length = gr.Slider(10, 500, value=50, step=10, label="Longueur max")
                            gen_temperature = gr.Slider(0.1, 1.5, value=0.7, step=0.1, label="Température (créativité)")
                        gen_button = gr.Button("Générer le texte", variant="primary")
                    gen_output = gr.Textbox(label="Texte Généré", interactive=False, scale=2)

                gen_button.click(
                    fn=api_client.generate_text,
                    inputs=[gen_input, gen_max_length, gen_temperature],
                    outputs=[gen_output]
                )
    return demo

# ==============================================================================
# 4. Point d'entrée de l'application
# ==============================================================================
if __name__ == "__main__":
    client = ApiClient(API_BASE_URL)
    app_ui = create_expert_ui(client)
    
    # Lancement du serveur Gradio
    app_ui.launch(server_name="0.0.0.0", server_port=7860)