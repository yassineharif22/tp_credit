# ==========================================================
# interface.py — Interface Streamlit connectée à l'API Flask
# Prérequis : app.py doit tourner sur http://127.0.0.1:5000
# Lancer : streamlit run interface.py
# ==========================================================
import streamlit as st
import requests
st.set_page_config(
    page_title="Demande de Crédit — Banque IA",
    page_icon="🏦",
    layout="centered"
)
st.title("🏦 Simulateur de Demande de Crédit")
st.markdown("Remplissez le formulaire. Notre modèle IA analysera votre profil et rendra une décision instantanée.")
st.divider()
st.subheader("📋 Informations du demandeur")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Âge", min_value=18, max_value=80, value=35, step=1)
    revenu_mensuel = st.number_input("Revenu mensuel (MAD)",
        min_value=1000, max_value=100000, value=12000, step=500)
    montant_credit_demande = st.number_input(
        "Montant du crédit demandé (MAD)",
        min_value=5000, max_value=500000,
        value=50000, step=5000)

with col2:
    duree_remboursement_mois = st.selectbox(
        "Durée de remboursement",
        options=[12, 24, 36, 48, 60],
        format_func=lambda x: f"{x} mois ({x // 12} an)",
        index=2
    )
    nb_credits_anterieurs = st.number_input(
        "Nombre de crédits antérieurs",
        min_value=0, max_value=10, value=0, step=1)
    situation_familiale = st.selectbox(
        "Situation familiale",
        options=["marie", "celibataire", "divorce"],
        format_func=lambda x: {
            "marie": "Marié(e)",
            "celibataire": "Célibataire",
            "divorce": "Divorcé(e)"
        }[x]
    )
    type_emploi = st.radio(
        "Type d'emploi",
        options=["fonctionnaire", "salarie_prive",
            "independant", "sans_emploi"],
        format_func=lambda x: {
            "fonctionnaire": "🏛️ Fonctionnaire",
            "salarie_prive": "🏢 Salarié privé",
            "independant": "💼 Indépendant",
            "sans_emploi": "❌ Sans emploi"
        }[x],
        horizontal=True
    )
st.divider()
if st.button("🔍 Soumettre ma demande", type="primary", use_container_width=True):
    # Construire le dictionnaire de données
    demande = {
        "age": age,
        "revenu_mensuel": revenu_mensuel,
        "montant_credit_demande": montant_credit_demande,
        "duree_remboursement_mois": duree_remboursement_mois,
        "nb_credits_anterieurs": nb_credits_anterieurs,
        "situation_familiale": situation_familiale,
        "type_emploi": type_emploi
    }
    # Appel à l'API Flask
    try:
        with st.spinner("Analyse en cours par le modèle IA..."):
            reponse = requests.post(
                "http://127.0.0.1:5000/predire",
                json=demande,
                timeout=10
            )
        # Traitement de la réponse
        if reponse.status_code == 200:
            resultat = reponse.json()
            decision = resultat["decision"]
            confiance = resultat["confiance"]
            st.divider()
            st.subheader("📊 Résultat de l'analyse")
            # Indicateur visuel vert = accordé
            if decision == "ACCORDÉ":
                st.markdown(
                    f"""<div style="background-color:#d4edda;
border:2px solid #28a745; border-radius:12px;
padding:24px; text-align:center;">

<h2 style="color:#155724;">✅ CRÉDIT ACCORDÉ</h2>
<p style="color:#155724; font-size:18px;">
Confiance : <strong>{confiance}</strong></p>
</div>""",
                    unsafe_allow_html=True
                )
            # Indicateur visuel rouge = refusé
            else:
                st.markdown(
                    f"""<div style="background-color:#f8d7da;
border:2px solid #dc3545; border-radius:12px;
padding:24px; text-align:center;">

<h2 style="color:#721c24;">❌ CRÉDIT REFUSÉ</h2>
<p style="color:#721c24; font-size:18px;">
Confiance : <strong>{confiance}</strong></p>
</div>""",
                    unsafe_allow_html=True
                )
            # Récapitulatif chiffré
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Âge", f"{age} ans")
                st.metric("Revenu", f"{revenu_mensuel:,} MAD")
            with c2:
                st.metric("Montant", f"{montant_credit_demande:,} MAD")
                st.metric("Durée", f"{duree_remboursement_mois} mois")
            with c3:
                st.metric("Crédits antérieurs", nb_credits_anterieurs)
                st.metric("Emploi",
                    type_emploi.replace("_", " ").title())
    # Si Flask n'est pas lancé
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de contacter l'API Flask.")
        st.info("→ Vérifiez que app.py est lancé : python app.py")
    # Si l'API met trop de temps à répondre
    except requests.exceptions.Timeout:
        st.error("⏱️ L'API met trop de temps à répondre.")
        st.info("→ Relancez app.py et réessayez.")
# Pied de page
st.divider()
st.caption("Module 3 — Formation IA | Exercice : Interface Streamlit ↔ API Flask")