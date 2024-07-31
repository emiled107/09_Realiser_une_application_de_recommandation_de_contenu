import azure.functions as func
from azure.storage.blob import BlobServiceClient
from collaborative_filtering import CollaborativeFiltering
import pandas as pd
from io import BytesIO
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Lecture des fichiers envoyés via multipart/form-data
        articles_metadata = req.files['articles_metadata']
        clicks = req.files['clicks']

        # Convertir les données reçues en DataFrames
        articles_metadata_df = pd.read_csv(BytesIO(articles_metadata.read()))
        clicks_df = pd.read_csv(BytesIO(clicks.read()))

        # Initialisation de l'instance CollaborativeFiltering
        cf = CollaborativeFiltering(None, None)
        cf.clicks_df = clicks_df
        cf.articles_metadata_df = articles_metadata_df

        # Exécution du pipeline d'entraînement
        training_results = cf.run_pipeline()  # Assurez-vous que cette méthode renvoie des informations sur l'entraînement

        # Connexion à Azure Blob Storage
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "your-container-name"

        # Transfert du modèle SVD
        with open("svd_model.joblib", "rb") as model_file:
            model_blob_client = blob_service_client.get_blob_client(container=container_name, blob="svd_model.joblib")
            model_blob_client.upload_blob(model_file, overwrite=True)

        # Transfert de la matrice d'interaction
        with open("user_article_matrix.csv", "rb") as matrix_file:
            matrix_blob_client = blob_service_client.get_blob_client(container=container_name, blob="user_article_matrix.csv")
            matrix_blob_client.upload_blob(matrix_file, overwrite=True)

        # Créer un message de retour avec les résultats de l'entraînement
        response_message = {
            "message": "Modèle et matrice initialisés et entraînés avec succès, et sauvegardés dans Blob Storage.",
            "training_details": training_results
        }
        return func.HttpResponse(json.dumps(response_message), status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Erreur: {str(e)}", status_code=500)
