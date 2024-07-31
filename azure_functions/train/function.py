import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO
import json
import logging

def train(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Connexion à Azure Blob Storage
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "projet09"

        # Lecture des fichiers envoyés via multipart/form-data
        articles_metadata = req.files['articles_metadata']
        clicks = req.files['clicks']

        # Convertir les données reçues en DataFrames
        articles_metadata_df = pd.read_csv(BytesIO(articles_metadata.read()))
        clicks_df = pd.read_csv(BytesIO(clicks.read()))

        # Utiliser le DataFrame pour quelque traitement, ici juste un exemple
        # Traitement hypothétique, remplacez par votre logique
        processed_data = process_data(articles_metadata_df, clicks_df)

        # Enregistrement du DataFrame traité dans Blob Storage
        save_data_to_blob(blob_service_client, container_name, processed_data)

        return func.HttpResponse("Traitement réussi et données sauvegardées", status_code=200)

    except Exception as e:
        logging.error(f"Erreur lors du traitement: {str(e)}")
        return func.HttpResponse(f"Erreur lors du traitement: {str(e)}", status_code=500)

def process_data(articles_df, clicks_df):
    return articles_df.merge(clicks_df, on="article_id")

def save_data_to_blob(blob_service_client, container_name, data):
    # Conversion du DataFrame en CSV et sauvegarde dans Blob Storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob="processed_data.csv")
    csv_data = data.to_csv(index=False)
    blob_client.upload_blob(csv_data, overwrite=True)
