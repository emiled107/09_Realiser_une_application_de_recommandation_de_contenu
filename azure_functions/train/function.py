import azure.functions as func
from azure.storage.blob import BlobServiceClient
from collaborative_filtering import CollaborativeFiltering
import os
import pandas as pd
from io import BytesIO

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Connexion à Azure Blob Storage
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "your-container-name"

        # Télécharge les données directement dans des DataFrames
        articles_metadata_blob_client = blob_service_client.get_blob_client(container=container_name, blob="articles_metadata.csv")
        clicks_blob_client = blob_service_client.get_blob_client(container=container_name, blob="clicks.csv")
        
        # Lire le contenu des blobs dans des DataFrames
        articles_metadata_stream = articles_metadata_blob_client.download_blob().readall()
        articles_metadata_df = pd.read_csv(BytesIO(articles_metadata_stream))

        clicks_stream = clicks_blob_client.download_blob().readall()
        clicks_df = pd.read_csv(BytesIO(clicks_stream))

        # Initialisation de l'instance CollaborativeFiltering
        cf = CollaborativeFiltering(None, None)
        cf.clicks_df = clicks_df
        cf.articles_metadata_df = articles_metadata_df

        # Exécution du pipeline d'entraînement
        cf.run_pipeline()  # Cette méthode sauvegarde le modèle et la matrice d'interaction utilisateur-article

        # On suppose que run_pipeline sauvegarde déjà le modèle localement, nous devons le transférer à Blob
        with open("svd_model.joblib", "rb") as model_file:
            model_blob_client = blob_service_client.get_blob_client(container=container_name, blob="svd_model.joblib")
            model_blob_client.upload_blob(model_file, overwrite=True)

        # De même pour la matrice d'interaction utilisateur-article
        with open("user_article_matrix.csv", "rb") as matrix_file:
            matrix_blob_client = blob_service_client.get_blob_client(container=container_name, blob="user_article_matrix.csv")
            matrix_blob_client.upload_blob(matrix_file, overwrite=True)

        return func.HttpResponse("Modèle et matrice initialisés et entraînés avec succès, et sauvegardés dans Blob Storage.", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Erreur: {str(e)}", status_code=500)
