from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/siret', methods=['GET'])
def get_siret_info():
    siren = request.args.get('siren')
    if not siren:
        return jsonify({"error": "Le paramètre 'siren' est requis."}), 400

    url = f"https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/{siren}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
