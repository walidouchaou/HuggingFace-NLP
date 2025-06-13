# ==============================================================================
# Etape 1: Base de l'image
# ==============================================================================
# Utilisation d'une image Python officielle. 'slim' est plus léger que la version standard.
FROM python:3.9-slim

# ==============================================================================
# Etape 2: Configuration de l'environnement
# ==============================================================================
# Empêche Python de bufferiser les logs, ce qui est mieux pour le logging de conteneur
ENV PYTHONUNBUFFERED 1

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# ==============================================================================
# Etape 3: Installation des dépendances
# ==============================================================================
# Copier d'abord le fichier de dépendances et les installer.
# Cette étape est mise en cache par Docker et ne sera ré-exécutée que si
# requirements.txt change, ce qui accélère les builds suivants.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==============================================================================
# Etape 4: Ajout du code de l'application
# ==============================================================================
# Copier le reste du code de l'application dans le conteneur
COPY . .

# ==============================================================================
# Etape 5: Sécurité et exécution
# ==============================================================================
# Création d'un utilisateur non-root pour des raisons de sécurité.
# Exécuter des conteneurs en tant que root est une mauvaise pratique.
RUN useradd --create-home appuser
USER appuser

# Exposition du port sur lequel l'application va tourner
EXPOSE 5000

# Commande pour démarrer l'application avec Gunicorn, un serveur WSGI de production.
# "run:app" fait référence à la variable 'app' dans le fichier 'run.py'.
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "run:app"] 