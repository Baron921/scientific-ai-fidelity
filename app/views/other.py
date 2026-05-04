import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_csv_data


def afficher():
    st.title("📈 Évaluation Avancée des Réécritures")
    st.markdown("Analyse multidimensionnelle de la qualité des textes générés par les différents prompts.")

    # 1. CHARGEMENT DES DONNÉES
    nom_du_fichier_csv = "factscores.csv"
    df = load_csv_data(nom_du_fichier_csv, separateur=",")

    if df is not None:

        # ==========================================================
        # SECTION 1 : SÉMANTIQUE ET COHÉRENCE
        # ==========================================================
        st.divider()  # Ligne de séparation
        st.header("🧠 Qualité Sémantique & Cohérence")
        st.markdown(
            "Mesure la proximité lexicale et la cohérence sémantique (Cosine, NLI, etc.) par rapport au texte source.")

        # Sélection des colonnes présentes dans le fichier factscores.csv
        colonnes_metrics = [
            "Cosine1", "Cosine2", "Cosine3",
            "NLI1", "NLI2", "NLI3",
            "FactScore1", "FactScore2", "FactScore3"
        ]

        # Sécurité : on garde uniquement les colonnes qui existent vraiment dans le CSV
        cols_existantes = [col for col in colonnes_metrics if col in df.columns]

        if cols_existantes:
            # Création des 4 tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Table 1 : Quartiles",
                "🔵 Fig 2 : Corrélations",
                "📦 Fig 3 : Distr. Cosine",
                "📦 Fig 4 : Distr. FactScore"
            ])

            # --- TAB 1 : TABLE DES QUARTILES ---
            with tab1:
                st.markdown("##### Table 1: Quartiles of semantic and textual coherence metrics across prompts")
                stats = df[cols_existantes].describe().T
                table_quartiles = stats[['25%', '50%', '75%', 'mean']].rename(columns={
                    '25%': 'Q1',
                    '50%': 'Q2 (Median)',
                    '75%': 'Q3',
                    'mean': 'Mean'
                })

                styled_table = table_quartiles.style.format("{:.2f}")
                st.dataframe(styled_table, use_container_width=True)

            # --- TAB 2 : MATRICE DE CORRÉLATION ---
            with tab2:
                st.markdown("##### Figure 2: Semantic and textual coherence metrics correlations")
                corr_matrix = df[cols_existantes].corr()

                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=".2f",
                    color_continuous_scale="Blues",
                    aspect="auto"
                )
                fig_corr.update_layout(xaxis_title="", yaxis_title="")
                st.plotly_chart(fig_corr, use_container_width=True)

            # --- TAB 3 : BOXPLOTS COSINE ---
            with tab3:
                st.markdown("##### Figure 3: Cosine Similarity boxplots across prompts")
                cols_cos = [c for c in cols_existantes if "Cosine" in c]
                if cols_cos:
                    df_cos = df[cols_cos].melt(var_name='Version', value_name='Score')
                    fig_cos = px.box(
                        df_cos, x="Score", y="Version", color="Version", orientation="h",
                        color_discrete_sequence=["#2c7bb6", "#fdae61", "#1a9641"]
                    )
                    fig_cos.update_layout(xaxis_title="Cosine Score", yaxis_title="")
                    st.plotly_chart(fig_cos, use_container_width=True)

            # --- TAB 4 : BOXPLOTS FACTSCORE ---
            with tab4:
                st.markdown("##### Figure 4: FactScore boxplots across prompts")
                cols_fact = [c for c in cols_existantes if "FactScore" in c]
                if cols_fact:
                    df_fact = df[cols_fact].melt(var_name='Version', value_name='Score')
                    fig_fact = px.box(
                        df_fact, x="Score", y="Version", color="Version", orientation="h",
                        color_discrete_sequence=["#2c7bb6", "#fdae61", "#1a9641"]
                    )
                    fig_fact.update_layout(xaxis_title="FactScore", yaxis_title="")
                    st.plotly_chart(fig_fact, use_container_width=True)
        else:
            st.warning("⚠️ Les colonnes attendues (Cosine, NLI, FactScore) ne sont pas trouvées dans le fichier.",
                       icon=":material/warning:")

        # ==========================================================
        # SECTION 2 : FIDÉLITÉ FACTUELLE
        # ==========================================================
        st.divider()
        st.header("🔎 Analyse de la Fidélité Factuelle")
        st.markdown(
            "Évalue si les réécritures respectent les faits du texte original sans introduire d'hallucinations.")

        c1, c2 = st.columns(2)

        with c1:
            st.info("**Taux de préservation factuelle**")
            try:
                # ⚠️ Attention: "fact_score_Rew1" n'est pas dans ton CSV factscores.csv
                # Tu devras soit adapter ces noms, soit charger un autre fichier !
                scores_factuels = pd.DataFrame({
                    "Modèle": ["Rew1", "Rew2", "Rew3"],
                    "Score de Fidélité": [df["fact_score_Rew1"].mean(), df["fact_score_Rew2"].mean(),
                                          df["fact_score_Rew3"].mean()]
                })

                fig_fact = px.line_polar(
                    scores_factuels,
                    r='Score de Fidélité',
                    theta='Modèle',
                    line_close=True,
                    title="Empreinte Factuelle par Modèle",
                    color_discrete_sequence=["#2ecc71"]
                )
                fig_fact.update_traces(fill='toself')
                st.plotly_chart(fig_fact, use_container_width=True)
            except KeyError:
                st.warning("⚠️ Colonnes factuelles manquantes (ex: fact_score_Rew1).", icon=":material/warning:")

        with c2:
            st.info("**Types d'erreurs (Hallucination vs Omission)**")
            st.write(
                "*(Ici, tu pourras insérer un graphique en barres empilées montrant la proportion d'ajouts et de suppressions par modèle)*")

        # ==========================================================
        # SECTION 3 : LLM AS A JUDGE
        # ==========================================================
        st.divider()
        st.header("⚖️ Évaluation par LLM (LLM as a Judge)")
        st.markdown(
            "Résultats de l'évaluation qualitative attribuée par un LLM arbitre sur des critères de fluidité, style et pertinence.")

        try:
            # ⚠️ Idem, ces colonnes ne sont pas dans factscores.csv
            df_judge = pd.DataFrame({
                "Rew1": df["llm_judge_Rew1"],
                "Rew2": df["llm_judge_Rew2"],
                "Rew3": df["llm_judge_Rew3"]
            }).melt(var_name="Modèle", value_name="Score (sur 5)")

            fig_judge = px.box(
                df_judge,
                x="Modèle",
                y="Score (sur 5)",
                color="Modèle",
                title="Distribution des notes attribuées par le LLM Juge",
                points="all",
                color_discrete_sequence=["#e74c3c", "#f39c12", "#2ecc71"]
            )
            fig_judge.update_layout(yaxis=dict(range=[0, 5.5]))
            st.plotly_chart(fig_judge, use_container_width=True)

        except KeyError:
            st.warning("⚠️ Colonnes du juge manquantes dans le CSV (ex: llm_judge_Rew1).", icon=":material/warning:")

    else:
        st.info("👈 En attente du fichier CSV pour afficher les graphiques.", icon=":material/folder_open:")



# def tracer_boxplot_factuel(metrique):
    #     if 'Domaine' in data.columns:
    #         # Récupère le nom des colonnes
    #         cols = ["Domaine", f"{metrique}1", f"{metrique}2", f"{metrique}3"]
    #
    #         if all(c in data.columns for c in cols):
    #             # 1. Équivalent du df_long = data.melt(...)
    #             df_long = data[cols].melt(id_vars='Domaine', var_name='Version', value_name=metrique)
    #
    #             # 2. Équivalent du sns.boxplot(...)
    #             fig = px.box(
    #                 df_long, x=metrique, y="Domaine", color="Version", orientation="h",
    #                 color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"],
    #                 title=f"Comparison of {metrique} across rewrites"  # 3. Titre exact !
    #             )
    #
    #             # Ajustements visuels pour correspondre au rendu matplotlib
    #             fig.update_layout(xaxis_title=metrique, yaxis_title="Domaine", boxmode="group")
    #             fig.update_yaxes(autorange="reversed")  # Trie les domaines de haut en bas
    #
    #             st.plotly_chart(fig, use_container_width=True)
    #         else:
    #             st.warning(f"⚠️ Colonnes {metrique} introuvables.")
    #
    #     # --- APPEL DES FONCTIONS (Équivalent des 3 dernières lignes de ton binôme) ---

    # --- FONCTION UTILITAIRE POUR LES BOXPLOTS ---

    import streamlit as st
    from components.menu import afficher_menu
    from views import home, data_view, eval_view, config_view, about_view, eval_metrics_view

    # ==========================================
    # CONFIGURATION GLOBALE
    # ==========================================
    st.set_page_config(
        page_title="TER ATAL - Évaluation Factuelle",
        page_icon="",
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
        case "Évaluation factuelle":
            eval_metrics_view.afficher()
        case "Configuration":
            config_view.afficher()
        case "À propos":
            about_view.afficher()
        case _:
            # Comportement par défaut (fallback) si erreur
            home.afficher()


import streamlit as st

def afficher_config():
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

    import streamlit as st

    from components.footer import afficher_footer

    def afficher():
        # En-tête principal
        st.markdown("<h1 style='text-align: center; color: #1E88E5;'>À propos</h1>",
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
            * **Adébiyi TOKOTCHI** *adebiyi-florias-jose.tokotchi@etu.univ-nantes.fr*
            * **Amos GANDONOU** *sedjro-amos.gandonou@etu.univ-nantes.fr*
            """)

        with col_encadrants:
            st.subheader("Encadrants")
            st.markdown("""
            
            """)

        afficher_footer()