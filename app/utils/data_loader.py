import os
import json
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(nom_fichier):
    """
    Charge et nettoie un fichier JSON situé dans le dossier data/json.
    Exemple d'utilisation : data = load_data("resultats_complets_ner_new.json")
    """

    # calcul du chemin absolu
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    racine_projet = os.path.dirname(dossier_actuel)

    # on ajoute le nom_fichier dynamique à la fin du chemin
    chemin_json = os.path.join(racine_projet, "../data", "json", nom_fichier)

    # ouverture et chargement sécurisé
    try:
        with open(chemin_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        st.error(f"❌ Fichier introuvable. Le système a cherché ici : {chemin_json}", icon=":material/error:")
        return None


@st.cache_data
def load_csv_data(nom_fichier, separateur=","):
    """
    Charge les données d'un fichier CSV situé dans le dossier data/csv.
    Utilise le cache de Streamlit pour ne pas recharger le fichier à chaque interaction.

    Arguments:
    - nom_fichier (str): Le nom de ton fichier (ex: "metriques.csv").
    - separateur (str): Le caractère de séparation (par défaut la virgule ',').
                        Mets ';' si ton CSV a été généré par Excel en français.

    Retourne:
    - pd.DataFrame: Les données sous forme de tableau, ou None si échec.
    """

    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    racine_projet = os.path.dirname(dossier_actuel)

    # On cible le dossier data/csv au lieu de data/json
    chemin_csv = os.path.join(racine_projet, "../data", "csv", nom_fichier)

    try:
        if not os.path.exists(chemin_csv):
            st.warning(f"⚠️ Fichier introuvable. Le système a cherché ici : {chemin_csv}", icon=":material/warning:")
            return None

        # Lecture du fichier CSV avec Pandas (en forçant l'encodage pour les accents)
        df = pd.read_csv(chemin_csv, sep=separateur, encoding="utf-8")
        return df

    except pd.errors.EmptyDataError:
        st.error(f"⚠️ Le fichier CSV est vide : {chemin_csv}", icon=":material/warning:")
        return None
    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier CSV '{nom_fichier}' : {e}", icon=":material/error:")
        return None