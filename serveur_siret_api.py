from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Bienvenue sur l'API SIRET/SIREN."})

@app.route("/siren/<siren>")
def get_siren_info(siren):
    url = f"https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/{siren}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Numéro SIREN introuvable ou erreur API."}), 404

    data = response.json()["unite_legale"]
    return jsonify({
        "siren": data.get("siren"),
        "nom_entreprise": data.get("denomination") or data.get("nom") or "Non disponible",
        "code_naf": data.get("activite_principale"),
        "libelle_naf": data.get("libelle_activite_principale", "Non disponible")
    })
