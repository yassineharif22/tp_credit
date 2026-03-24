import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

# ============================================
# 1. Chargement et séparation des données
# ============================================
print("📂 Chargement du dataset...")
df = pd.read_csv("credit_dataset.csv")

print(f"✅ Dataset chargé : {df.shape[0]} demandes, {df.shape[1]} colonnes")
print(f"\nAperçu des données :")
print(df.head())
print(f"\nDistribution de la cible (decision) :")
print(df["decision"].value_counts())

# X = les features (colonnes d'entrée)
# y = la cible (ce qu'on veut prédire)
X = df.drop(columns=["decision"])
y = df["decision"]

# 80% pour entraîner, 20% pour tester
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n✅ Données séparées : {X_train.shape[0]} entraînement, {X_test.shape[0]} test")

# ============================================
# 2. Construction du Pipeline Scikit-learn
# ============================================
print("\n🔧 Construction du pipeline...")

# Colonnes numériques → on normalise (même échelle)
colonnes_num = [
    "age", 
    "revenu_mensuel", 
    "montant_credit_demande",
    "duree_remboursement_mois", 
    "nb_credits_anterieurs"
]

# Colonnes catégorielles → on encode en 0/1
colonnes_cat = ["situation_familiale", "type_emploi"]

preprocesseur = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), colonnes_num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), colonnes_cat)
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocesseur", preprocesseur),
        ("modele", RandomForestClassifier(n_estimators=100, random_state=42))
    ]
)

print("✅ Pipeline créé")

# ============================================
# 3. Entraînement et évaluation
# ============================================
print("\n🚀 Entraînement du modèle...")
pipeline.fit(X_train, y_train)
print("✅ Entraînement terminé")

# Prédiction sur les données de test
print("\n📊 Évaluation sur les données de test...")
y_pred = pipeline.predict(X_test)

# Affichage des résultats
accuracy = accuracy_score(y_test, y_pred)
print(f"\n📈 Accuracy : {accuracy:.2%}")
print("\n📋 Rapport détaillé :")
print(classification_report(
    y_test, 
    y_pred,
    target_names=["Refusé ❌", "Accordé ✅"]
))

# ============================================
# 4. Sauvegarde du modèle
# ============================================
print("\n💾 Sauvegarde du modèle...")
with open("model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("✅ Modèle sauvegardé dans model.pkl")
print("\n" + "="*50)
print("🎉 Entraînement réussi !")
print("="*50)
