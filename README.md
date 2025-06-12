# HuggingFace-NLP
Ce projet met en œuvre des modèles Transformer via l'écosystème Hugging Face pour des tâches de Traitement Automatique du Langage Naturel.  Il couvre la classification de sentiment , la génération de texte, le question-réponse , ainsi que l'analyse comparative de différents modèles.

## Démarrage rapide

Construisez l'image Docker et lancez-la :

```bash
docker build -t hf-nlp-demo .
docker run -p 5000:5000 -p 7860:7860 hf-nlp-demo
```

La partie API est disponible sur `http://localhost:5000` et l'interface Gradio sur `http://localhost:7860`.
