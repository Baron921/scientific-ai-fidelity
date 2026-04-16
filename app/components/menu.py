import streamlit as st
from streamlit_option_menu import option_menu


def afficher_menu():
    with st.sidebar:
        # st.markdown("### Navigation")
        selected = option_menu(
            menu_title="Menu Principal",
            options=["Accueil", "Données", "Évaluation", "Configuration", "À propos"],
            icons=["house", "database-fill-up", "play-circle", "sliders", "info-circle"],
            menu_icon="cast",
            default_index=0,  # Évaluation par défaut
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#007BFF", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#007BFF", "color": "white", "icon-color": "white"},
            }
        )
    return selected
