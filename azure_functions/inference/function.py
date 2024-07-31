import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
from .collaborative_filtering import CollaborativeFiltering 

def load_model_from_blob():
    """Charge le modèle SVD depuis Azure Blob Storage dans 'projet09'."""
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name = 'projet09'
    blob_name = 'model/svd_model.joblib'
    
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    # Télécharge le modèle dans un fichier temporaire
    model_path = '/tmp/svd_model.joblib'
    with open(model_path, "wb") as model_file:
        model_file.write(blob_client.download_blob().readall())
    
    return model_path

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        user_id = req.params.get('user_id')
        if not user_id:
            return func.HttpResponse("Please pass a user_id on the query string", status_code=400)

        # Chargement du modèle
        model_path = load_model_from_blob()
        cf = CollaborativeFiltering(None, None)
        cf.load_model(model_path)  # Charge le modèle

        # Prédiction des recommandations
        recommendations = cf.predict(user_id)

        return func.HttpResponse(json.dumps({"user_id": user_id, "recommendations": recommendations}), status_code=200)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
