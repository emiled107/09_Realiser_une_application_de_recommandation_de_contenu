# Utiliser une image de base officielle Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port sur lequel Flask s'exécute
EXPOSE 5000

# Définir la commande pour démarrer l'application
CMD ["python", "app.py"]
