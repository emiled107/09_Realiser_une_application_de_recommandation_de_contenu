import logging
import os
from collaborative_filtering import CollaborativeFiltering

def main():
    logging.basicConfig(level=logging.INFO)

    # Chemins vers les fichiers de données et emplacements de sauvegarde
    data_dir = '../data/'
    model_dir = '../models/'
    articles_metadata_path = os.path.join(data_dir, 'articles_metadata.csv')
    clicks_path = os.path.join(data_dir, 'clicks_sample.csv')
    model_path = os.path.join(model_dir, 'svd_model.joblib')
    matrix_path = os.path.join(model_dir, 'user_article_matrix.csv')

    # Initialisation de la classe CollaborativeFiltering
    cf = CollaborativeFiltering(articles_metadata_path, clicks_path)

    # Chargement et préparation des données
    clicks_df, articles_metadata_df = cf.load_data()
    clicks_df = cf.clean_and_prepare_data(clicks_df)
    interaction_matrix = cf.build_interaction_matrix(clicks_df)

    # Entraînement du modèle et évaluation
    cf.train_model(interaction_matrix)
    rmse, mae, r2, correlation = cf.evaluate_model(interaction_matrix)
    logging.info(f"Évaluation du modèle: RMSE: {rmse}, MAE: {mae}, R2: {r2}, Correlation: {correlation}")

    # Sauvegarde du modèle et de la matrice d'interaction
    cf.save_model(model_path)
    cf.save_user_article_matrix(matrix_path)

    logging.info("Entraînement terminé et modèles sauvegardés.")

if __name__ == "__main__":
    main()
