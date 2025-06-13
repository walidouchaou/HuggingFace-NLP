# NLP API avec Flask et Transformers

Ce projet expose plusieurs modèles NLP de Hugging Face via une API RESTful construite avec Flask. L'architecture est conçue pour être modulaire, scalable et prête pour le déploiement avec Docker.

## Architecture du Projet

Le projet est divisé en deux composants principaux :

-   **`/app`**: Le backend Flask.
    -   `__init__.py`: Application Factory qui assemble l'application.
    -   `config.py`: Gère la configuration via des variables d'environnement.
    -   `services.py`: Module pour les services externes (ici, le chargement des modèles NLP).
    -   `routes.py`: Définit les endpoints de l'API avec un Blueprint.
-   **`/frontend`**: Un client web simple (HTML, CSS, JS) pour interagir avec l'API.
-   **`/gradio_app.py`**: Une interface de démonstration alternative avec Gradio.

Fichiers principaux à la racine :
-   `run.py`: Point d'entrée pour lancer le serveur Flask (pour le développement).
-   `Dockerfile`: Instructions pour construire l'image Docker de l'application backend.
-   `requirements.txt`: Dépendances Python du backend.
-   `.env.example`: Fichier d'exemple pour la configuration d'environnement.

## Démarrage Rapide

### 1. Pré-requis

-   Python 3.8+
-   Docker (recommandé pour la production)

### 2. Installation des dépendances

```bash
# Créez et activez un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installez les dépendances Python
pip install -r requirements.txt
```

### 3. Configuration

Copiez le fichier d'exemple `.env.example` et renommez-le en `.env`. Vous pouvez y surcharger les modèles par défaut si besoin.

```bash
cp .env.example .env
```

### 4. Lancer l'application

#### Option A: En Développement (Backend + Frontend Gradio)

1.  **Lancez le serveur backend Flask :**

    Dans un premier terminal, lancez l'API. Elle tournera sur `http://127.0.0.1:5000`.

    ```bash
    python run.py
    ```

2.  **Lancez l'interface Gradio :**

    Dans un second terminal, lancez l'interface Gradio.

    ```bash
    python gradio_app.py
    ```

    Ouvrez ensuite l'URL fournie par Gradio (généralement `http://127.0.0.1:7860`) dans votre navigateur.

#### Option B: En Production (Backend avec Docker)

1.  **Construire et lancer l'image Docker du backend :**

    ```bash
    # Construire l'image
    docker build -t nlp-api .
    
    # Lancer le conteneur. L'API sera accessible sur http://localhost:5000
    docker run -p 5000:5000 nlp-api
    ```

2.  **Lancer le client Gradio localement :**

    Pendant que le conteneur Docker tourne, lancez l'interface Gradio dans un autre terminal. Elle se connectera à l'API du conteneur.

    ```bash
    python gradio_app.py
    ```
    
    Ouvrez l'URL de Gradio dans votre navigateur pour utiliser l'application.
