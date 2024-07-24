from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    response = requests.get(f"<URL_AZURE_FUNCTION>?user_id={user_id}")
    recommendations = response.json()
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
