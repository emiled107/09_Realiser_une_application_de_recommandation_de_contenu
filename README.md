# My Content - Recommender System

## Description

My Content est une start-up qui veut encourager la lecture en recommandant des contenus pertinents pour ses utilisateurs. Ce projet implémente un système de recommandation d'articles et de livres en utilisant Azure Functions pour la partie serverless.

## Structure du Projet

- `app`: Contient l'application Flask pour l'interface utilisateur.
- `azure_functions`: Contient les Azure Functions pour le système de recommandation.
- `data`: Contient les données d'articles et d'interactions utilisateurs.
- `models`: Contient le modèle de recommandation entraîné.
- `scripts`: Contient les scripts pour le prétraitement des données et l'entraînement du modèle.
- `docs`: Contient la documentation et les présentations.

## Installation

1. Cloner le repository
2. Installer les dépendances

```bash
pip install -r app/requirements.txt
