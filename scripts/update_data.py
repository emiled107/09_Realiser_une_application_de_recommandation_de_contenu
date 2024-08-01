import logging
import os
from collaborative_filtering import CollaborativeFiltering

def main():
    logging.basicConfig(level=logging.INFO)

    # Chemins vers les fichiers et répertoires
    data_dir = '../data/'
    model_dir = '../models/'
    new_clicks_path = os.path.join(data_dir, 'clicks')  # Répertoire contenant les nouveaux fichiers de clics
    model_path = os.path.join(model_dir, 'svd_model.joblib')
    matrix_path = os.path.join(model_dir, 'user_article_matrix.csv')

    # Initialisation de la classe CollaborativeFiltering avec des chemins None car on chargera les modèles/matrices existants
    cf = CollaborativeFiltering(None, new_clicks_path)

    # Chargement du modèle et de la matrice d'interaction existants
    cf.load_model(model_path)
    cf.load_user_article_matrix(matrix_path)

    # Mise à jour des données avec les nouveaux clics
    cf.update_data()

    # Réentraînement du modèle avec la matrice d'interaction mise à jour
    cf.retrain_model()

    # Sauvegarde du modèle réentrainé et de la matrice mise à jour
    cf.save_model(model_path)
    cf.save_user_article_matrix(matrix_path)

    logging.info("Réentraînement terminé et modèles sauvegardés.")

if __name__ == "__main__":
    main()
