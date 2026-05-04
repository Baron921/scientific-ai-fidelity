import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt


def afficher_factuel(data):
    st.header("Analyse de la fidélité factuelle")
    # st.divider()
    # st.markdown("Évaluation de la préservation des faits et détection d'hallucinations via différentes métriques.")

    # On récupère la liste des métriques activées via les toggles
    filtres = st.session_state.get('filtre_factuel',
                                   ["FactCC", "FactAcc", "DAE", "FactScore", "NLI", "Cosine", "NaiveMatch", "BertScore",
                                    "BartScore"])

    titres_onglets = ["Table 2 : Seuils"]

    if "FactAcc" in filtres: titres_onglets.append("FactAcc")
    if "DAE" in filtres: titres_onglets.append("DAE")
    if "FactCC" in filtres: titres_onglets.append("FactCC")
    if "BertScore" in filtres: titres_onglets.append("BertScore")
    if "BartScore" in filtres: titres_onglets.append("BartScore")

    # Création physique des onglets
    onglets = st.tabs(titres_onglets)

    # On utilise un "index" pour savoir dans quel onglet écrire
    idx = 0

    # --- TAB : TABLE DES SEUILS ---
    with onglets[idx]:
        st.markdown("##### Table 2 : Global part of rewrites that meets significancy threshold of 0.85")

        configurations_metriques = [
            ("FactCC", lambda df, i: df[f"FactCC{i}"] >= 0.85),
            ("FactAcc", lambda df, i: df[f"FactAcc{i}"] >= 0.85),
            ("DAE", lambda df, i: df[f"DAE{i}"] >= 0.85),
            ("FactScore",
             lambda df, i: (df[f"FactScore{i}"] >= 0.85) & (df[f"NLI{i}"] >= 0.85) & (df[f"Cosine{i}"] >= 0.85) & (
                         df[f"Naive{i}"] >= 0.85)),
            ("NLI ≤ 0", lambda df, i: df[f"NLI{i}"] < 0),
            ("NLI ≥ 0.85", lambda df, i: df[f"NLI{i}"] >= 0.85),
            ("Cosine", lambda df, i: df[f"Cosine{i}"] >= 0.85),
            ("NaiveMatch", lambda df, i: df[f"Naive{i}"] >= 0.85)
        ]

        lignes_tableau = []
        total_rows = len(data)

        if total_rows > 0:
            for nom_affichage, condition in configurations_metriques:
                row = {'Metric': nom_affichage}
                for i in [1, 2, 3]:
                    try:
                        nb_succes = data.loc[condition(data, i)].shape[0]
                        row[f"Rew {i}"] = nb_succes / total_rows
                    except KeyError:
                        row[f"Rew {i}"] = None
                lignes_tableau.append(row)

            if lignes_tableau:
                df_thresh = pd.DataFrame(lignes_tableau).set_index('Metric')
                styled_thresh = df_thresh.style.format("{:.1%}")
                #styled_thresh = styled_thresh.background_gradient(subset=['Rew 1', 'Rew 2', 'Rew 3'], axis=1)

                def highlight_max_row(s):
                    is_max = s == s.max()
                    return ['font-weight: bold;' if v else '' for v in is_max]

                styled_thresh = styled_thresh.apply(highlight_max_row, subset=['Rew 1', 'Rew 2', 'Rew 3'], axis=1)
                st.dataframe(styled_thresh, use_container_width=True)
            else:
                st.warning("⚠️ Aucune métrique factuelle n'a été trouvée dans les données.")
        else:
            st.error("Le jeu de données est vide.")

    idx += 1

    # --- FONCTION UTILITAIRE SEABORN ---
    def tracer_boxplot_factuel(metrique, *vline):
        if 'Domaine' in data.columns:
            cols = [f"{metrique}1", f"{metrique}2", f"{metrique}3"]

            if all(c in data.columns for c in cols):
                # Melt en incluant la colonne Domaine
                df_long = data[["Domaine"] + cols].melt(
                    id_vars=["Domaine"],
                    value_vars=cols,
                    var_name="Version",
                    value_name=metrique
                )

                fig, ax = plt.subplots(figsize=(10, 6))

                sns.boxplot(
                    data=df_long,
                    y="Domaine",
                    x=metrique,
                    hue="Version",
                    ax=ax,
                    palette=["#1f77b4", "#ff7f0e", "#2ca02c"]
                )

                if vline:
                    for val in vline:
                        ax.axvline(x=val, linestyle="--", linewidth=1.5)
                        ax.text(val, ax.get_ylim()[1] / 2, f"{val}", rotation=0, va='bottom', fontsize=10)

                ax.set_title(f"Comparison of {metrique} across rewrites")
                plt.tight_layout()

                st.pyplot(fig)
            else:
                st.warning(f"⚠️ Colonnes {metrique} introuvables.")

    # --- TABS DYNAMIQUES POUR LES BOXPLOTS ---
    if "FactAcc" in filtres:
        with onglets[idx]:
            st.markdown("##### FactAcc boxplots across prompts")
            tracer_boxplot_factuel("FactAcc")
        idx += 1

    if "DAE" in filtres:
        with onglets[idx]:
            st.markdown("##### DAE boxplots across prompts")
            tracer_boxplot_factuel("DAE")
        idx += 1

    if "FactCC" in filtres:
        with onglets[idx]:
            st.markdown("##### FactCC boxplots across prompts")
            tracer_boxplot_factuel("FactCC")
        idx += 1

    if "BertScore" in filtres:
        with onglets[idx]:
            st.markdown("##### BertScore boxplots across prompts")
            tracer_boxplot_factuel("BertScore", 0.85, 0.9)  # Appel avec 2 seuils
        idx += 1

    if "BartScore" in filtres:
        with onglets[idx]:
            st.markdown("##### BartScore boxplots across prompts")
            tracer_boxplot_factuel("BartScore", -1.5)  # Appel avec 1 seuil
        idx += 1