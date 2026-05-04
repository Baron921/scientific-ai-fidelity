import streamlit as st
from views import config_view
from components.menu import afficher_menu
from views import eval_metrics_view, data_view, home, eval_view, about_view

st.set_page_config(page_title="Dashboard d'Évaluation", layout="wide")

page_selectionnee = afficher_menu()

# --- ROUTAGE ---
match page_selectionnee:
    case "Accueil":
        home.afficher()
    case "Données":
        data_view.afficher()
    case "NER":
        eval_view.afficher()
    case "Metrics":
        eval_metrics_view.afficher()
    case "Configuration":
        config_view.afficher_config()
    case "À propos":
        about_view.afficher_apropos()
    case _:
        # Comportement par défaut (fallback) si erreur
        home.afficher()
