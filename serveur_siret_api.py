from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Bienvenue sur l'API SIRET/SIREN."})

@app.route("/siren/<siren>")
def get_siren_info(siren):
    try:
        url = f"https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/{siren}"
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": "Numéro SIREN introuvable ou erreur API."}), 404

        unite_legale = response.json().get("unite_legale", {})
        
        return jsonify({
            "siren": unite_legale.get("siren", "Non disponible"),
            "nom_entreprise": unite_legale.get("denomination") or unite_legale.get("nom") or "Non disponible",
            "code_naf": unite_legale.get("activite_principale", "Non disponible"),
            "libelle_naf": unite_legale.get("libelle_activite_principale", "Non disponible")
        })
    
    except Exception as e:
        # Ceci s'affiche dans les logs Render
        print(f"Erreur serveur : {e}")
        return jsonify({"error": "Erreur interne du serveur."}), 500
