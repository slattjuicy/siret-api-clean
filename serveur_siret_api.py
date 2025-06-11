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
        print(f"[INFO] Requête envoyée à : {url}")
        response = requests.get(url)
        print(f"[INFO] Status code : {response.status_code}")

        if response.status_code != 200:
            print(f"[ERROR] Réponse invalide : {response.text}")
            return jsonify({"error": "Numéro SIREN introuvable ou erreur API."}), 404

        json_data = response.json()
        unite_legale = json_data.get("unite_legale", {})

        print(f"[INFO] Données reçues : {unite_legale}")

        return jsonify({
            "siren": unite_legale.get("siren", "Non disponible"),
            "nom_entreprise": unite_legale.get("denomination") or unite_legale.get("nom") or "Non disponible",
            "code_naf": unite_legale.get("activite_principale", "Non disponible"),
            "libelle_naf": unite_legale.get("libelle_activite_principale", "Non disponible")
        })

    except Exception as e:
        print(f"[EXCEPTION] Une erreur est survenue : {e}")
        return jsonify({"error": "Erreur interne du serveur."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
