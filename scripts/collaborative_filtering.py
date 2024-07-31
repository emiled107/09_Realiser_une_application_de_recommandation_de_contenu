import pandas as pd
import numpy as np
import logging
import os
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr
import mlflow
import mlflow.sklearn  # Pour l'intégration avec MLflow
import joblib  # Pour la sauvegarde du modèle

class CollaborativeFiltering:
    def __init__(self, articles_metadata_path, clicks_path, n_components=100):
        self.articles_metadata_path = articles_metadata_path
        self.clicks_path = clicks_path
        self.n_components = n_components
        self.user_article_matrix = None
        self.svd_model = None
        self.clicks_df = None
        self.articles_metadata_df = None

    def load_data(self):
        articles_metadata_df = pd.read_csv(self.articles_metadata_path)
        if os.path.isfile(self.clicks_path):
            clicks_df = pd.read_csv(self.clicks_path)
        elif os.path.isdir(self.clicks_path):
            clicks_dfs = []
            for filename in os.listdir(self.clicks_path):
                if filename.endswith('.csv'):
                    file_path = os.path.join(self.clicks_path, filename)
                    clicks_dfs.append(pd.read_csv(file_path))
            clicks_df = pd.concat(clicks_dfs, ignore_index=True)
        else:
            raise ValueError(f"Le chemin {self.clicks_path} n'est ni un fichier ni un répertoire valide.")
        return clicks_df, articles_metadata_df

    def clean_and_prepare_data(self, clicks_df):
        clicks_df.drop_duplicates(inplace=True)
        clicks_df.dropna(inplace=True)
        return clicks_df

    def build_interaction_matrix(self, clicks_df):
        return pd.pivot_table(clicks_df, index='user_id', columns='click_article_id', aggfunc=len, fill_value=0)

    def train_model(self, interaction_matrix):
        num_features = interaction_matrix.shape[1]
        n_components = min(self.n_components, num_features - 1)
        self.svd_model = TruncatedSVD(n_components=n_components)
        self.svd_model.fit(interaction_matrix)
        logging.info("Modèle entraîné avec succès")

    def evaluate_model(self, interaction_matrix):
        # Vérifiez que le modèle est chargé
        if self.svd_model is None:
            logging.error("Le modèle n'est pas chargé.")
            raise ValueError("Le modèle n'est pas chargé.")

        # Créez une matrice d'interactions utilisateur-article pour évaluer le modèle
        num_users, num_items = interaction_matrix.shape
        all_predictions = np.zeros((num_users, num_items))

        # Prédictions pour chaque utilisateur
        for user_index in range(num_users):
            user_vector = interaction_matrix.iloc[user_index, :].values.reshape(1, -1)
            predicted_vector = self.predict(user_index, user_vector)  # Prédiction pour un utilisateur
            all_predictions[user_index, :] = predicted_vector

        # Récupérer les valeurs réelles
        true_values = interaction_matrix.to_numpy().flatten()
        predicted_values = all_predictions.flatten()

        # Calculer les métriques
        rmse = np.sqrt(mean_squared_error(true_values, predicted_values))
        mae = mean_absolute_error(true_values, predicted_values)
        r2 = r2_score(true_values, predicted_values)
        correlation, _ = pearsonr(true_values, predicted_values)

        return rmse, mae, r2, correlation


    def save_model(self, filename='svd_model.joblib'):
        if self.svd_model:
            joblib.dump(self.svd_model, filename)
            logging.info(f'Modèle sauvegardé sous {filename}')
        else:
            logging.error("Aucun modèle à sauvegarder.")

    def load_model(self, filename='svd_model.joblib'):
        self.svd_model = joblib.load(filename)
        logging.info(f'Modèle chargé depuis {filename}')

    def predict(self, user_index, user_interaction_matrix):
        """ Fait des prédictions basées sur la matrice d'interaction de l'utilisateur. """
        if self.svd_model:
            # Si user_interaction_matrix est un DataFrame, convertir en ndarray
            if isinstance(user_interaction_matrix, pd.DataFrame):
                user_interaction_matrix = user_interaction_matrix.values

            predictions = self.svd_model.transform(user_interaction_matrix)
            return self.svd_model.inverse_transform(predictions).flatten()
        else:
            logging.error("Aucun modèle chargé pour faire des prédictions.")
            return np.zeros(user_interaction_matrix.shape[1])

    def update_data(self):
        """ Mise à jour de la matrice d'interaction avec de nouvelles interactions utilisateur-article. """
        clicks_df, _ = self.load_data()
        clicks_df = self.clean_and_prepare_data(clicks_df)
        new_interaction_matrix = self.build_interaction_matrix(clicks_df)
        if self.user_article_matrix is None:
            self.user_article_matrix = new_interaction_matrix
        else:
            self.user_article_matrix += new_interaction_matrix
        logging.info("Données mises à jour avec de nouvelles interactions.")

    def load_user_article_matrix(self, matrix_path):
        """ Charge la matrice d'interaction utilisateur-article depuis un fichier. """
        self.user_article_matrix = pd.read_csv(matrix_path, index_col=0)
        logging.info(f"Matrice d'interaction chargée depuis {matrix_path}")

    def save_user_article_matrix(self, matrix_path):
        """ Sauvegarde la matrice d'interaction utilisateur-article dans un fichier. """
        if self.user_article_matrix is not None:
            self.user_article_matrix.to_csv(matrix_path)
            logging.info(f"Matrice d'interaction sauvegardée sous {matrix_path}")
        else:
            logging.error("Aucune matrice d'interaction à sauvegarder.")

    def retrain_model(self):
        """ Réentraînement du modèle SVD avec la matrice d'interaction mise à jour. """
        if self.user_article_matrix is not None and not self.user_article_matrix.empty:
            num_features = self.user_article_matrix.shape[1]
            n_components = min(self.n_components, num_features - 1)
            self.svd_model = TruncatedSVD(n_components=n_components)
            self.svd_model.fit(self.user_article_matrix)
            logging.info("Modèle réentraîné avec succès.")
        else:
            logging.error("Aucune matrice d'interaction pour réentraîner le modèle.")

    def run_pipeline(self):
        """ Pipeline complet d'entraînement du modèle avec MLflow. """
        mlflow.set_experiment('Collaborative_Filtering_Experiment')
        with mlflow.start_run():
            clicks_df = self.clean_and_prepare_data(clicks_df)
            interaction_matrix = self.build_interaction_matrix(clicks_df)
            self.train_model(interaction_matrix)
            rmse, mae, r2, correlation = self.evaluate_model(interaction_matrix)

            # Log metrics
            mlflow.log_metric("RMSE", rmse)
            mlflow.log_metric("MAE", mae)
            mlflow.log_metric("R2_Score", r2)
            mlflow.log_metric("Correlation", correlation)

            self.save_model()  # Sauvegarder le modèle avec joblib et MLflow
            self.save_user_article_matrix('user_article_matrix.csv')
            mlflow.end_run()
