import streamlit as st
import pandas as pd
from components.footer import afficher_footer
from components.header import afficher_header
from utils.data_loader import load_data, load_csv_data
from views.sections.semantique import afficher_semantique
from views.sections.factuel import afficher_factuel
from views.sections.llm_judge import afficher_llm_judge


def afficher():
    afficher_header(
        titre="Évaluation Avancée des Réécritures",
        icone="",
        description="Analyse multidimensionnelle de la qualité des textes générés par les différents prompts"
    )

    # ==========================================================
    # PRÉPARATION DES DONNÉES GLOBALES (Le cœur du réacteur)
    # ==========================================================
    metrics_raw = load_data("metrics.json")
    llmj_raw = load_data("llm_judgment3.json")
    facts_raw = load_csv_data("factscores.csv", separateur=",")

    if metrics_raw is not None and llmj_raw is not None and facts_raw is not None:

        # Traitement de metrics.json
        metrics = pd.DataFrame(metrics_raw)
        idx_drop = metrics[((metrics["Licence"] == "CC BY-SA 4.0") & (metrics["Domaine"] == "CHEMICAL"))].index
        metrics = metrics.drop(idx_drop).reset_index(drop=True)

        cols_to_drop = ['Doi', 'Auteur', 'Date de publication', 'URL', 'Licence', 'URL / PDF', 'Sous-domaine']
        metrics.drop(columns=[c for c in cols_to_drop if c in metrics.columns], errors='ignore', inplace=True)

        # Traitement de llm_judgment3.json
        llmj = pd.DataFrame(llmj_raw)
        llmj = llmj.drop(idx_drop).reset_index(drop=True)

        # Traitement de factscores.csv
        facts = facts_raw.copy()
        cols_fact_drop = ["FactScore1", "FactScore2", "FactScore3"]
        facts = facts.drop(columns=[c for c in cols_fact_drop if c in facts.columns], errors='ignore')
        facts = facts.drop(idx_drop).reset_index(drop=True)

        # FUSION FINALE
        data = pd.concat([metrics, llmj, facts], axis=1)

        data = data.loc[:, ~data.columns.duplicated()]

        # ==========================================================
        # APPEL DES SECTIONS (Injection du DataFrame)
        # ==========================================================
        afficher_semantique(data)
        afficher_factuel(data)
        afficher_llm_judge(data)

    else:
        st.error("❌ Impossible de charger un ou plusieurs fichiers de données (metrics, llm_judgment, factscores).")

    afficher_footer()