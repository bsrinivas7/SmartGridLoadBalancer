from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
LOAD_BALANCER_URL = os.getenv('LOAD_BALANCER_URL', 'http://load_balancer:5000')

@app.route('/charge', methods=['POST'])
def charge_request():
    try:
        # Get least loaded substation from load balancer
        response = requests.get(f"{LOAD_BALANCER_URL}/get_substation")
        substation_url = response.json()['substation_url']

        # Forward request to substation
        charge_response = requests.post(
            f"{substation_url}/charge",
            json=request.json,
            timeout=5
        )
        return jsonify(charge_response.json()), charge_response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
