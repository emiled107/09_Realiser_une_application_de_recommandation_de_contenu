import azure.functions as func
from azure.storage.blob import BlobServiceClient
from collaborative_filtering import CollaborativeFiltering
import pandas as pd
from io import BytesIO

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
        cf.clicks_df = clicks_df  # Assurez-vous que CollaborativeFiltering peut traiter les DataFrame directement
        cf.articles_metadata_df = articles_metadata_df

        # Exécution du pipeline d'entraînement
        cf.run_pipeline()  # Cette méthode doit sauvegarder le modèle et la matrice d'interaction utilisateur-article

        # Sauvegarde du modèle et de la matrice dans Azure Blob Storage si nécessaire
        # Supposons que la méthode run_pipeline sauvegarde les données localement,
        # vous devrez transférer ces fichiers vers Blob Storage comme montré ci-dessous
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

        return func.HttpResponse("Modèle et matrice initialisés et entraînés avec succès, et sauvegardés dans Blob Storage.", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Erreur: {str(e)}", status_code=500)
