# 🏦 API Crédit — Prototype d'Automatisation des Demandes de Crédit

Bienvenue! Ce projet implémente une **API Flask intelligente** pour l'automatisation du pré-traitement des demandes de crédit utilisant un **modèle Machine Learning**.

## 📋 Description

Une banque marocaine souhaite automatiser l'analyse des demandes de crédit. Ce prototype :
- ✅ Reçoit les informations d'un demandeur (âge, revenu, montant, etc.)
- ✅ Applique un modèle ML (Random Forest) pour évaluer le risque
- ✅ Retourne une décision : **ACCORDÉ** ou **REFUSÉ** avec un score de confiance

## 📁 Structure du Projet

```
tp_credit/
├── credit_dataset.csv       # 300 demandes fictives pour entraînement
├── train_model.py           # Script d'entraînement du modèle ML
├── app.py                   # Serveur Flask (API)
├── tester_api.py            # Tests de l'API
└── README.md                # Ce fichier
```

## 🚀 Installation & Mise en Place

### 1️⃣ Installer les dépendances

```bash
pip install flask scikit-learn pandas requests
```

### 2️⃣ Entraîner le modèle

Exécutez d'abord le script d'entraînement :

```bash
python train_model.py
```

✅ Cela va :
- Charger les 300 demandes de crédit
- Entraîner un modèle Random Forest
- Créer un fichier `model.pkl` (le modèle sauvegardé)

Vous devriez voir une **accuracy autour de 90%**.

### 3️⃣ Démarrer l'API Flask

```bash
python app.py
```

Vous devriez voir :
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

## 🧪 Tester l'API

### Option 1 : Depuis le navigateur

Ouvrez votre navigateur et allez à :
- **http://127.0.0.1:5000/** → Message d'accueil
- **http://127.0.0.1:5000/demo** → Exemples de requêtes
- **http://127.0.0.1:5000/statistiques** → Statistiques du dataset

### Option 2 : Script Python (recommandé)

Dans un **autre terminal**, exécutez :

```bash
python tester_api.py
```

Cela lancera 7 tests complets de l'API.

### Option 3 : cURL

```bash
curl -X POST http://127.0.0.1:5000/predire \
  -H "Content-Type: application/json" \
  -d '{
    "age": 38,
    "revenu_mensuel": 18000,
    "montant_credit_demande": 40000,
    "duree_remboursement_mois": 24,
    "nb_credits_anterieurs": 0,
    "situation_familiale": "marie",
    "type_emploi": "fonctionnaire"
  }'
```

## 📊 Routes de l'API

### 1. **GET /** — Accueil

```bash
curl http://127.0.0.1:5000/
```

**Réponse** :
```json
{
  "message": "API crédit — opérationnelle ✅",
  "routes": {
    "POST /predire": "Soumettre une demande de crédit",
    "GET /statistiques": "Statistiques du dataset",
    "GET /demo": "Voir un exemple"
  }
}
```

### 2. **POST /predire** — Prédiction

Soumet une demande et reçoit une décision.

**Requête** :
```json
{
  "age": 38,
  "revenu_mensuel": 18000,
  "montant_credit_demande": 40000,
  "duree_remboursement_mois": 24,
  "nb_credits_anterieurs": 0,
  "situation_familiale": "marie",
  "type_emploi": "fonctionnaire"
}
```

**Réponse** :
```json
{
  "decision": "ACCORDÉ ✅",
  "confiance": "99.0%",
  "timestamp": "2026-03-21T10:30:45.123456"
}
```

### 3. **GET /statistiques** — Données du modèle

```bash
curl http://127.0.0.1:5000/statistiques
```

**Réponse** :
```json
{
  "statistiques_dataset": {
    "total_demandes": 300,
    "demandes_accordees": 234,
    "demandes_refusees": 66,
    "taux_accord": "78.0%",
    "revenu_moyen_accordes": "12345.67 MAD"
  }
}
```

### 4. **GET /historique** — Dernières prédictions

```bash
curl http://127.0.0.1:5000/historique
```

Retourne les 10 dernières prédictions.

### 5. **GET /demo** — Exemples de requêtes

Voir les structures attendues (avec valeurs d'exemple).

## 📖 Description du Dataset

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `age` | Numérique | Âge (18-80) | 35 |
| `revenu_mensuel` | Numérique | En MAD | 12000 |
| `montant_credit_demande` | Numérique | En MAD | 50000 |
| `duree_remboursement_mois` | Numérique | 12-60 mois | 36 |
| `nb_credits_anterieurs` | Numérique | Crédits passés | 1 |
| `situation_familiale` | Catégorique | celibataire / marie / divorce | marie |
| `type_emploi` | Catégorique | salarie_prive / fonctionnaire / independant / sans_emploi | fonctionnaire |
| `decision` | Cible (0/1) | 1 = accordé, 0 = refusé | 1 |

## ✅ Validations Obligatoires

L'API valide automatiquement les données reçues :

- ✅ **Âge** : 18 à 80 ans
- ✅ **Revenu** : > 0 MAD
- ✅ **Montant crédit** : > 0 MAD
- ✅ **Durée** : 12 à 60 mois
- ✅ **Situation familiale** : celibataire / marie / divorce
- ✅ **Type emploi** : salarie_prive / fonctionnaire / independant / sans_emploi

## 🔧 Pipeline Machine Learning

```
Input Data
    ↓
┌─────────────────────────────────┐
│     Preprocessing               │
│  - StandardScaler (numerical)   │
│  - OneHotEncoder (categorical)  │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│   RandomForestClassifier        │
│   (100 decision trees)          │
└─────────────────────────────────┘
    ↓
Decision + Confidence Score
```

## 🎯 Cas de Teste

### Cas 1 : Profil Favorable ✅

```python
{
    "age": 38,
    "revenu_mensuel": 18000,
    "montant_credit_demande": 40000,
    "duree_remboursement_mois": 24,
    "nb_credits_anterieurs": 0,
    "situation_familiale": "marie",
    "type_emploi": "fonctionnaire"
}
```
**Résultat attendu** : `ACCORDÉ ✅` (~99%)

### Cas 2 : Profil Défavorable ❌

```python
{
    "age": 24,
    "revenu_mensuel": 4000,
    "montant_credit_demande": 150000,
    "duree_remboursement_mois": 60,
    "nb_credits_anterieurs": 3,
    "situation_familiale": "celibataire",
    "type_emploi": "sans_emploi"
}
```
**Résultat attendu** : `REFUSÉ ❌` (~75%)

## 🎓 Exercices d'Approfondissement

Je recommande de continuer avec ces exercices :

### ⭐ Exercice 1 — Validation avancée
Améliorer les validations (déjà implémentées dans cette version)

### ⭐⭐ Exercice 2 — Route /statistiques
Afficher plus de statistiques sur le dataset (déjà implémentée)

### ⭐⭐ Exercice 3 — Historique des prédictions
Enregistrer les prédictions dans une liste (déjà implémentée)

### ⭐⭐⭐ Exercice 4 — Interface Streamlit
Créer une interface visuelle connectée à l'API :

```bash
pip install streamlit
```

Puis créer `interface.py` :

```python
import streamlit as st
import requests

st.title("💳 Demande de Crédit - Interface")

age = st.number_input("Âge", 18, 80, 35)
revenu = st.number_input("Revenu mensuel (MAD)", 0, 1000000, 10000)
montant = st.number_input("Montant demandé (MAD)", 0, 1000000, 50000)
duree = st.select_slider("Durée (mois)", [12, 24, 36, 48, 60])
credits = st.number_input("Crédits antérieurs", 0, 10, 0)
situation = st.selectbox("Situation", ["celibataire", "marie", "divorce"])
emploi = st.selectbox("Type d'emploi", 
    ["salarie_prive", "fonctionnaire", "independant", "sans_emploi"])

if st.button("📊 Soumettre la demande"):
    data = {
        "age": age,
        "revenu_mensuel": revenu,
        "montant_credit_demande": montant,
        "duree_remboursement_mois": duree,
        "nb_credits_anterieurs": credits,
        "situation_familiale": situation,
        "type_emploi": emploi
    }
    
    response = requests.post("http://127.0.0.1:5000/predire", json=data)
    result = response.json()
    
    if result["decision"] == "ACCORDÉ ✅":
        st.success(f'Decision: {result["decision"]} - Confiance: {result["confiance"]}')
    else:
        st.error(f'Decision: {result["decision"]} - Confiance: {result["confiance"]}')
```

Lancez avec :
```bash
streamlit run interface.py
```

## 📝 Fichiers Générés

Après exécution :
- ✅ `model.pkl` — Le modèle ML sauvegardé
- ✅ Syslog Flask au démarrage de `app.py`

## 🐛 Dépannage

### Erreur : `model.pkl` introuvable
```
Exécutez d'abord : python train_model.py
```

### Erreur : Port 5000 déjà utilisé
```bash
# Utiliser un autre port
python -c "from app import app; app.run(port=5001)"
```

### Erreur : Module non trouvé (flask, sklearn, pandas)
```bash
pip install flask scikit-learn pandas requests
```

## 📖 Ressources

- 📚 [Flask Documentation](https://flask.palletsprojects.com/)
- 🤖 [Scikit-learn Documentation](https://scikit-learn.org/)
- 📊 [Pandas Documentation](https://pandas.pydata.org/)

## ✨ Réalisé par

**Prototype d'API Crédit** — Automation de demandes de crédit
- ✅ Modèle ML : Random Forest
- ✅ Framework Web : Flask
- ✅ Données : 300 demandes fictives
- ✅ Accuracy : ~90%

---

**Bon développement ! 🚀** 

Pour toute question, consultez les commentaires dans le code ou les ressources ci-dessus.
