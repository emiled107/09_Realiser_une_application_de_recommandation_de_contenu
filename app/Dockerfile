FROM python:3.8-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

COPY . /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    pkg-config \
    libhdf5-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances et installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port que l'application utilisera
EXPOSE 5000

# Commande pour lancer l'application
CMD ["sh", "-c", "python app.py"]