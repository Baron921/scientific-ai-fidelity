import streamlit as st


def afficher():
    # En-tête principal
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>À propos de notre technologie</h1>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem; color: #555;'>Sécuriser la réécriture scientifique générée par l'Intelligence Artificielle.</p>",
        unsafe_allow_html=True)

    st.write("")
    st.divider()
    st.write("")

    # Contexte du projet
    st.markdown("""
    Ce projet a été réalisé dans le cadre du **Travail d'Étude et de Recherche (TER)** du Master 1 Apprentissage et Traitement Automatique de la Langue (ATAL) de Nantes Université, dans l'optique de **mesurer la fréquence des erreurs factuelles dans les réécritures scientifiques produites par l'IA et de tester des méthodes simples pour les détecter automatiquement**.
    """)

    st.write("")
    st.write("")

    # Informations de contact
    col_etudiants, col_encadrants = st.columns(2)

    with col_etudiants:
        st.subheader("Étudiants")
        st.markdown("""
        * **Florias Tokotchi** *florias.tokotchi@etu.univ-nantes.fr* *(à remplacer par ton vrai mail si besoin)*
        * **Amos** *amos.[nom]@etu.univ-nantes.fr* *(à compléter)*
        """)

    with col_encadrants:
        st.subheader("Encadrants")
        st.markdown("""
        * **Richard Dufour** *richard.dufour@univ-nantes.fr*
        * **Florian Boudin** *florian.boudin@inria.fr*
        """)

    st.write("")
    st.divider()
    st.caption("Version 1.0.0 | © 2026 Projet TER ATAL - Nantes Université")