from app import create_app

# Crée une instance de l'application en utilisant la factory
app = create_app()

if __name__ == "__main__":
    # Lancement du serveur de développement Flask.
    # Ne pas utiliser en production. Utilisez un serveur WSGI comme Gunicorn.
    # Exemple de commande Gunicorn :
    # gunicorn --workers 4 --bind 0.0.0.0:5000 "run:app"
    app.run(host="0.0.0.0", port=5000, debug=True) 