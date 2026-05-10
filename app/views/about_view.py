import streamlit as st
from components.footer import afficher_footer
from components.header import afficher_header


def afficher_apropos():
    afficher_header(
        titre="A propos du projet",
        icone="",
        description="Contexte, méthodologie et équipe"
    )

    st.markdown("""
            Ce projet a été réalisé dans le cadre du **Travail d'Étude et de Recherche (TER)** du Master 1 Apprentissage et Traitement Automatique de la Langue (ATAL) de Nantes Université, dans l'optique de **mesurer la fréquence des erreurs factuelles dans les réécritures scientifiques produites par l'IA et de tester des méthodes simples pour les détecter automatiquement**.
            """)

    st.write("")

    st.link_button("Voir le code source sur GitHub", "https://github.com/Baron921/scientific-ai-fidelity.git",
                   use_container_width=True)

    st.write("")

    st.markdown("### Stack Technique")

    col_tech1, col_tech2, col_tech3, col_tech4 = st.columns(4)
    with col_tech1:
        st.markdown("**Langage**\n- Python 3")
    with col_tech2:
        st.markdown("**Interface**\n- Streamlit\n- Bootstrap Icons")
    with col_tech3:
        st.markdown("**Data & Calcul**\n- Pandas\n- NumPy")
    with col_tech4:
        st.markdown("**Visualisation**\n- Plotly\n- Seaborn & Matplotlib")

    st.divider()

    st.markdown("### Équipe & Encadrement")

    st.markdown("##### Projet réalisé par :")
    col_team1, col_team2 = st.columns(2)
    with col_team1:
        st.success("**Adébiyi TOKOTCHI**\n\n*adebiyi-florias-jose.tokotchi@etu.univ-nantes.fr*\n\n*Étudiant / Master 1 ATAL*")
    with col_team2:
        st.success("**Amos GANDONOU**\n\n*sedjro-amos.gandonou@etu.univ-nantes.fr*\n\n*Étudiant / Master 1 ATAL*")

    st.write("")

    st.markdown("##### Sous la supervision de :")
    col_enc1, col_enc2 = st.columns(2)  # Tu peux mettre st.columns(1) si tu n'as qu'un seul encadrant
    with col_enc1:
        st.info("**Richard DUFOUR**\n\n*richard.dufour@univ-nantes.fr*\n\n*Professeur agrégé au LS2N, Université de Nantes | Chercheur à Inria*")
    with col_enc2:
        st.info("**Florian BOUDIN**\n\n*florian.boudin@inria.fr*\n\n*Professeur des Universités | TALN / NLP @ LS2N | Nantes Université*")

    st.write("")

    afficher_footer()