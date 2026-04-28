import streamlit as st

def afficher():
    st.header("Configuration du Pipeline")
    st.write("Personnalisez les méthodes d'évaluation utilisées lors de l'analyse des textes.")

    # Initialisation des variables de configuration dans le session_state
    if 'config' not in st.session_state:
        st.session_state.config = {
            "use_rouge": True,
            "use_scibert": False,
            "use_ner": True,
            "use_triplets": True,
            "use_factcc": False,
            "threshold": 0.85
        }

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Baselines")
        st.session_state.config["use_rouge"] = st.toggle(
            "Activer ROUGE-L (Similarité syntaxique)",
            value=st.session_state.config["use_rouge"]
        )
        st.session_state.config["use_scibert"] = st.toggle(
            "Activer SciBERTScore (Sémantique)",
            value=st.session_state.config["use_scibert"]
        )

    with col2:
        st.subheader("Extraction Structurée")
        st.session_state.config["use_ner"] = st.toggle(
            "Vérification NER (Chiffres & Unités)",
            value=st.session_state.config["use_ner"]
        )
        st.session_state.config["use_triplets"] = st.toggle(
            "Vérification par Triplets Relationnels",
            value=st.session_state.config["use_triplets"]
        )

    st.divider()

    st.subheader("Paramètres Avancés")
    st.session_state.config["threshold"] = st.slider(
        "Seuil de tolérance factuelle",
        0.0, 1.0,
        st.session_state.config["threshold"],
        help="Définit le score en dessous duquel une alerte d'hallucination est déclenchée."
    )

    st.success("La configuration est automatiquement sauvegardée pour l'onglet Évaluation.")