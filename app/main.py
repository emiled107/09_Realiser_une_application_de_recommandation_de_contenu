from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    user_id = request.form['user_id']
    # URL de la fonction Azure déployée
    azure_function_url = 'https://your-azure-function-url.azurewebsites.net/api/GetRecommendations'
    # Appel à la fonction Azure avec l'ID utilisateur
    response = requests.post(azure_function_url, json={'user_id': user_id})
    recommendations = response.json()
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
