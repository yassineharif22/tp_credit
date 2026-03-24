import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("="*70)
print("🧪 TESTS DE L'API CRÉDIT")
print("="*70)

# Test 1: Accueil
print("\n1️⃣  Test de l'accueil (GET /)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Erreur : {e}")

# Test 2: Route de démonstration
print("\n2️⃣  Test de la démo (GET /demo)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/demo")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False)[:500] + "...")
except Exception as e:
    print(f"❌ Erreur : {e}")

# Test 3: Prédiction cas 1 (Accord)
print("\n3️⃣  Test de prédiction - CAS 1 (Profil favorable)")
print("-" * 70)
demande_1 = {
    "age": 38,
    "revenu_mensuel": 18000,
    "montant_credit_demande": 40000,
    "duree_remboursement_mois": 24,
    "nb_credits_anterieurs": 0,
    "situation_familiale": "marie",
    "type_emploi": "fonctionnaire"
}
print(f"Demande : {json.dumps(demande_1, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(f"{BASE_URL}/predire", json=demande_1)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Erreur : {e}")

# Test 4: Prédiction cas 2 (Refus)
print("\n4️⃣  Test de prédiction - CAS 2 (Profil défavorable)")
print("-" * 70)
demande_2 = {
    "age": 24,
    "revenu_mensuel": 4000,
    "montant_credit_demande": 150000,
    "duree_remboursement_mois": 60,
    "nb_credits_anterieurs": 3,
    "situation_familiale": "celibataire",
    "type_emploi": "sans_emploi"
}
print(f"Demande : {json.dumps(demande_2, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(f"{BASE_URL}/predire", json=demande_2)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Erreur : {e}")

# Test 5: Validation d'erreur (âge invalide)
print("\n5️⃣  Test de validation - Âge invalide (< 18)")
print("-" * 70)
demande_invalide = {
    "age": 15,
    "revenu_mensuel": 5000,
    "montant_credit_demande": 20000,
    "duree_remboursement_mois": 24,
    "nb_credits_anterieurs": 0,
    "situation_familiale": "celibataire",
    "type_emploi": "salarie_prive"
}
try:
    response = requests.post(f"{BASE_URL}/predire", json=demande_invalide)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Erreur : {e}")

# Test 6: Historique
print("\n6️⃣  Test de l'historique (GET /historique)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/historique")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total de prédictions : {data['total_predictions']}")
    print(f"Dernières prédictions : {len(data['dernieres_predictions'])}")
except Exception as e:
    print(f"❌ Erreur : {e}")

# Test 7: Statistiques
print("\n7️⃣  Test des statistiques (GET /statistiques)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/statistiques")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Erreur : {e}")

print("\n" + "="*70)
print("✅ Tests terminés !")
print("="*70)
