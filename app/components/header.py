import streamlit as st


def afficher_header(titre, icone="", description=None):
    st.title(f"{icone} {titre}")

    # Affichage optionnel d'une description sous le titre
    if description:
        st.markdown(f"{description}")

    st.divider()