# Utiliser une image de base Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et installer les dépendances
COPY ./app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY ./app /app

# Exposer le port sur lequel l'application Flask s'exécute
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "app.py"]
