import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "POST":
        try:
            req_body = req.get_json()
            # Traitez ici les données reçues
        except ValueError:
            return func.HttpResponse("Données incorrectes", status_code=400)
        return func.HttpResponse(f"Données reçues et traitées {req_body}", status_code=200)
    else:
        return func.HttpResponse("Méthode non autorisée", status_code=405)
