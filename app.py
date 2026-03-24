from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os
from datetime import datetime

# ============================================
# 1. Initialisation et chargement du modèle
# ============================================
app = Flask(__name__)

# Charger le modèle une seule fois au démarrage
print("📂 Chargement du modèle...")
try:
    with open("model.pkl", "rb") as f:
        modele = pickle.load(f)
    print("✅ Modèle chargé avec succès")
except FileNotFoundError:
    print("❌ Erreur : model.pkl introuvable")
    print("   Veuillez d'abord exécuter : python train_model.py")
    exit(1)

# Historique des prédictions (en mémoire)
historique = []

# ============================================
# 2. Route d'accueil (GET /)
# ============================================
@app.route("/", methods=["GET"])
def accueil():
    return jsonify({
        "message": "API crédit — opérationnelle ✅",
        "version": "1.0",
        "routes": {
            "POST /predire": "Soumettre une demande de crédit",
            "GET /": "Message d'accueil",
            "GET /demo": "Voir un exemple de requête",
            "GET /historique": "Voir les 10 dernières prédictions",
            "GET /statistiques": "Statistiques du dataset"
        }
    })

# ============================================
# 3. Route de démonstration (GET /demo)
# ============================================
@app.route("/demo", methods=["GET"])
def demo():
    return jsonify({
        "description": "Exemples de requêtes POST pour /predire",
        "exemple_1_accord": {
            "profil": "Haut revenu, stable",
            "donnees": {
                "age": 38,
                "revenu_mensuel": 18000,
                "montant_credit_demande": 40000,
                "duree_remboursement_mois": 24,
                "nb_credits_anterieurs": 0,
                "situation_familiale": "marie",
                "type_emploi": "fonctionnaire"
            }
        },
        "exemple_2_refus": {
            "profil": "Bas revenu, endettement élevé",
            "donnees": {
                "age": 24,
                "revenu_mensuel": 4000,
                "montant_credit_demande": 150000,
                "duree_remboursement_mois": 60,
                "nb_credits_anterieurs": 3,
                "situation_familiale": "celibataire",
                "type_emploi": "sans_emploi"
            }
        },
        "valeurs_acceptees": {
            "situation_familiale": ["celibataire", "marie", "divorce"],
            "type_emploi": ["salarie_prive", "fonctionnaire", "independant", "sans_emploi"]
        }
    })

# ============================================
# 4. Route de prédiction (POST /predire)
# ============================================
@app.route("/predire", methods=["POST"])
def predire():
    # Récupérer les données JSON envoyées
    donnees = request.get_json()

    # Vérification basique
    if not donnees:
        return jsonify({"erreur": "Aucune donnée reçue"}), 400

    # Vérification des champs obligatoires
    champs_obligatoires = [
        "age", "revenu_mensuel", "montant_credit_demande",
        "duree_remboursement_mois", "nb_credits_anterieurs",
        "situation_familiale", "type_emploi"
    ]
    
    champs_manquants = [c for c in champs_obligatoires if c not in donnees]
    if champs_manquants:
        return jsonify({
            "erreur": f"Champs manquants : {', '.join(champs_manquants)}"
        }), 400

    # Validation des valeurs
    try:
        age = int(donnees.get("age"))
        if age < 18 or age > 80:
            return jsonify({"erreur": "L'âge doit être entre 18 et 80 ans"}), 400

        revenu = float(donnees.get("revenu_mensuel"))
        if revenu <= 0:
            return jsonify({"erreur": "Le revenu doit être positif"}), 400

        montant = float(donnees.get("montant_credit_demande"))
        if montant <= 0:
            return jsonify({"erreur": "Le montant doit être positif"}), 400

        duree = int(donnees.get("duree_remboursement_mois"))
        if duree < 12 or duree > 60:
            return jsonify({"erreur": "La durée doit être entre 12 et 60 mois"}), 400

        nb_credits = int(donnees.get("nb_credits_anterieurs"))
        if nb_credits < 0:
            return jsonify({"erreur": "Le nombre de crédits antérieurs doit être positif"}), 400

        situation = donnees.get("situation_familiale")
        if situation not in ["celibataire", "marie", "divorce"]:
            return jsonify({"erreur": "Situation familiale invalide"}), 400

        type_emploi = donnees.get("type_emploi")
        if type_emploi not in ["salarie_prive", "fonctionnaire", "independant", "sans_emploi"]:
            return jsonify({"erreur": "Type d'emploi invalide"}), 400

    except (ValueError, TypeError) as e:
        return jsonify({"erreur": f"Erreur de validation : {str(e)}"}), 400

    # Convertir en DataFrame pour Scikit-learn
    df_demande = pd.DataFrame([donnees])

    try:
        # Prédiction et probabilité de confiance
        prediction = modele.predict(df_demande)[0]
        probabilites = modele.predict_proba(df_demande)[0]
        confiance = round(float(max(probabilites)) * 100, 1)

        # Construire la réponse
        decision = "ACCORDÉ ✅" if prediction == 1 else "REFUSÉ ❌"

        resultat = {
            "decision": decision,
            "confiance": f"{confiance}%",
            "timestamp": datetime.now().isoformat()
        }

        # Ajouter à l'historique
        historique.append({
            **donnees,
            **resultat
        })

        return jsonify(resultat), 200

    except Exception as e:
        return jsonify({"erreur": f"Erreur lors de la prédiction : {str(e)}"}), 500

# ============================================
# 5. Route d'historique (GET /historique)
# ============================================
@app.route("/historique", methods=["GET"])
def get_historique():
    # Retourner les 10 dernières prédictions
    dernieres = historique[-10:]
    return jsonify({
        "total_predictions": len(historique),
        "dernieres_predictions": dernieres
    })

# ============================================
# 6. Route de statistiques (GET /statistiques)
# ============================================
@app.route("/statistiques", methods=["GET"])
def statistiques():
    try:
        df = pd.read_csv("credit_dataset.csv")

        total = int(len(df))
        accordes = int((df["decision"] == 1).sum())
        refuses = int((df["decision"] == 0).sum())
        taux_accord = (accordes / total) * 100

        revenu_accordes = float(df[df["decision"] == 1]["revenu_mensuel"].mean())
        revenu_refuses = float(df[df["decision"] == 0]["revenu_mensuel"].mean())
        age_moyen = float(df["age"].mean())

        return jsonify({
            "statistiques_dataset": {
                "total_demandes": total,
                "demandes_accordees": accordes,
                "demandes_refusees": refuses,
                "taux_accord": f"{taux_accord:.1f}%",
                "age_moyen": f"{age_moyen:.1f}",
                "revenu_moyen_accordes": f"{revenu_accordes:.2f} MAD",
                "revenu_moyen_refuses": f"{revenu_refuses:.2f} MAD"
            },
            "modele": {
                "type": "RandomForestClassifier",
                "features": 7,
                "predictions_api": len(historique)
            }
        })
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500

# ============================================
# 7. Route d'erreur 404
# ============================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "erreur": "Route non trouvée",
        "message": "Utilise GET / pour voir les routes disponibles"
    }), 404

# ============================================
# 8. Démarrage du serveur
# ============================================
# ✅ Compatible déploiement
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)