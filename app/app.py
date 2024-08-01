from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Liste des IDs utilisateurs disponibles pour la sélection
    user_ids = [i for i in range(707)]  # Adaptez cette liste selon vos données
    return render_template('index.html', user_ids=user_ids)

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    user_id = request.form['user_id']
    # URL de la fonction Azure déployée
    azure_function_url = 'https://cfmodel.azurewebsites.net/api/HttpTrigger_predict'
    # Appel à la fonction Azure avec l'ID utilisateur
    response = requests.post(azure_function_url, json={'user_id': user_id})
    recommendations = response.json()
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
