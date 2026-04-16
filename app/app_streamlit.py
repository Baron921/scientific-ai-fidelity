import streamlit as st

# Importation de tes propres modules
from components.menu import afficher_menu
from views import home, data_view, eval_view, config_view, about_view

# ==========================================
# CONFIGURATION GLOBALE
# ==========================================
st.set_page_config(
    page_title="TER ATAL - Évaluation Factuelle",
    page_icon="🔬",
    layout="wide"
)

# Initialisation de la mémoire de l'application
if 'dataset' not in st.session_state:
    st.session_state.dataset = None

# ==========================================
# ROUTAGE DE L'APPLICATION
# ==========================================
# On récupère le choix fait dans le fichier menu.py
page_selectionnee = afficher_menu()

# On affiche le contenu du fichier correspondant

# ROUTAGE DE L'APPLICATION
# ==========================================
match page_selectionnee:
    case "Accueil":
        home.afficher()
    case "Données":
        data_view.afficher()
    case "Évaluation":
        eval_view.afficher()
    case "Configuration":
        config_view.afficher()
    case "À propos":
        about_view.afficher()
    case _:
        # Comportement par défaut (fallback) si erreur
        home.afficher()