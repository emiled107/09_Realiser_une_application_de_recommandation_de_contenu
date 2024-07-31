import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from io import BytesIO

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Vérification de l'authentification
    auth_key = req.headers.get('Authorization')
    expected_auth_key = "Basic emiled:01projet09"

    if auth_key != expected_auth_key:
        return func.HttpResponse("Unauthorized", status_code=401)

    # Récupération du fichier du modèle depuis la requête
    try:
        file_stream = BytesIO(req.get_body())
        file_name = req.headers.get('x-filename') 
        if not file_name:
            return func.HttpResponse("File name not provided in headers.", status_code=400)
    except Exception as e:
        return func.HttpResponse(f"Error reading file: {str(e)}", status_code=400)

    # Téléchargement du fichier sur Azure Blob Storage
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name = 'projet09'
    blob_name = file_name  

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Lecture du fichier et téléchargement
    try:
        blob_client.upload_blob(file_stream, overwrite=True)
        return func.HttpResponse(f"File {file_name} uploaded successfully.")
    except Exception as e:
        return func.HttpResponse(f"Failed to upload file: {str(e)}", status_code=500)
